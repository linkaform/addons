# coding: utf-8
"""Armado de los argumentos con los que se invoca un script.

El contrato lo fija el back real en backend/scripts/tasks.py:79 (`get_args`):

    ['python', script_path, record, simplejson.dumps(script_args), str(record_to_long)]

Cualquier diferencia aqui se vuelve una diferencia de comportamiento entre
correr un script en local y correrlo en produccion.
"""

import asyncio
import contextlib
import json
import re
import shlex

import settings
from errors import ContainerError, ScriptTimeout

_cache = {'docker_image': None}
_semaforo = {'sem': None}


def _limite():
    """Tope opcional de scripts corriendo a la vez (MINIBACK_MAX_CONCURRENT).

    Con 0 no hay tope, que es el default: el punto de esto es que el front
    pueda disparar sus llamadas en paralelo. Poner un tope solo si la maquina
    sufre, porque cada corrida es un proceso de python cargando linkaform_api.
    """
    if not settings.MAX_CONCURRENT:
        return contextlib.nullcontext()
    if _semaforo['sem'] is None:
        _semaforo['sem'] = asyncio.Semaphore(settings.MAX_CONCURRENT)
    return _semaforo['sem']


async def exec_async(cmd, timeout):
    """Corre un comando sin bloquear el event loop.

    Con subprocess.run el loop se congela mientras dura el `docker exec`, y
    Sanic no puede ni empezar a leer la siguiente peticion: 10 llamadas del
    front se vuelven 10 corridas en fila. Con subprocesos de asyncio el loop
    sigue libre y las corridas ocurren de verdad en paralelo.

    Devuelve (returncode, stdout, stderr) con los dos flujos ya decodificados.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError:
        raise ContainerError('no se encontro el binario `docker` dentro del mini-back')

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        # Matar el cliente de `docker exec` no mata al proceso dentro del
        # contenedor; el back real tiene la misma limitacion.
        proc.kill()
        await proc.wait()
        raise asyncio.TimeoutError()

    return (
        proc.returncode,
        stdout.decode('utf-8', 'replace'),
        stderr.decode('utf-8', 'replace'),
    )


async def docker_image():
    """Imagen del contenedor destino, para script_args['docker_image'].

    En el back sale de script.properties['container'] (tasks.py:158). Aqui se
    pregunta al contenedor y se cachea; si no se puede, se manda None en vez
    de tumbar la corrida: ningun script del repo lo usa para decidir nada.
    """
    if _cache['docker_image'] is not None:
        return _cache['docker_image']
    cmd = ['docker', 'inspect', '--format', '{{.Config.Image}}', settings.CONTAINER]
    try:
        returncode, stdout, _ = await exec_async(cmd, timeout=10)
        if returncode == 0:
            _cache['docker_image'] = stdout.strip()
    except Exception as e:
        print('miniback: no se pudo resolver la imagen de "{}": {}'.format(
            settings.CONTAINER, e))
    return _cache['docker_image']


def build_record(body):
    """Argumento 1: el record, siempre como string.

    Port de tasks.py:116-120. Ahi el record llega como string y le empalman
    el record_id recortando la llave de cierre. Se conserva esa mecanica; lo
    unico que se agrega es no intentar el empalme si el string no termina en
    '}' (en el back eso produce JSON invalido y el script revienta al parsear).
    """
    record = body.get('record') or ''
    record_id = body.get('record_id')

    if not record:
        return '{}'

    if isinstance(record, dict):
        record = dict(record)
        record['record_id'] = record_id
        return json.dumps(record)

    record = str(record)
    if record.rstrip().endswith('}'):
        record = record.rstrip()
        return record[:-1] + ', "record_id": "{}"'.format(record_id) + '}'
    return record


def build_script_args(body, auth_header, script_path):
    """Argumento 2, antes de serializar.

    El back arma script_args = {'data': <body completo>} (script_resource.py:717)
    y le agrega account_id, jwt, name y docker_image
    (script_resource.py:719-720/747, tasks.py:194-195). Los scripts leen su
    payload de self.data['data'].
    """
    account_id = body.get('account_id')
    if account_id in (None, ''):
        account_id = settings.ACCOUNT_ID

    return {
        'data': body,
        'jwt': auth_header or '',
        'account_id': account_id,
        'name': script_path.rsplit('/', 1)[-1],
        # Ya resuelta y cacheada al arrancar; aqui solo se lee.
        'docker_image': _cache['docker_image'],
    }


def build_args(body, auth_header, script_path):
    """Los tres argumentos del script, en orden.

    El tercero es el record_to_long de tasks.py:122: aqui siempre 'False',
    porque no se simula el corte del record por MAX_ARG_STRLEN.
    """
    return [
        build_record(body),
        json.dumps(build_script_args(body, auth_header, script_path)),
        'False',
    ]


def build_cmd(script_path, args):
    """El `docker exec` completo. Port de tasks.py:206-214, sin el `env time`
    del mtail, que solo sirve para la telemetria del servidor."""
    return ['docker', 'exec', settings.CONTAINER, 'python', script_path] + list(args)


def _log_salida(returncode, stdout, stderr):
    """stdout y stderr crudos, sin interpretar: lo que el script realmente
    escribio, antes de que format_output lo parta en response y log."""
    print('miniback: <<< returncode={}'.format(returncode))
    print('--- stdout ---')
    print(stdout if stdout else '(vacio)')
    print('--- stderr ---')
    print(stderr if stderr else '(vacio)')


async def run(script_path, args):
    """Corre el script en el contenedor destino.

    Devuelve (returncode, stdout, stderr). No interpreta nada: de eso se
    encargan format_output y get_exception_error.
    """
    cmd = build_cmd(script_path, args)
    # El comando queda impreso tal cual para poder pegarlo en una terminal y
    # reproducir la corrida a mano. Es el modo de depuracion principal.
    print('\nminiback: >>> {}'.format(' '.join(shlex.quote(part) for part in cmd)))

    async with _limite():
        try:
            returncode, stdout, stderr = await exec_async(cmd, settings.TIMEOUT)
        except asyncio.TimeoutError:
            raise ScriptTimeout(
                '{} paso de MINIBACK_TIMEOUT ({}s) y se cancelo'.format(
                    script_path.rsplit('/', 1)[-1], settings.TIMEOUT))

    _log_salida(returncode, stdout, stderr)

    # `docker exec` responde 125 cuando el problema es el contenedor, no el
    # script. Se distingue para no reportarlo como si el script hubiera fallado.
    if returncode == 125 or 'No such container' in stderr or 'is not running' in stderr:
        raise ContainerError(
            'no se pudo ejecutar en el contenedor "{}": {}'.format(
                settings.CONTAINER, stderr.strip() or 'returncode 125'))

    return returncode, stdout, stderr


def format_output(output):
    """Port de backend/base/utils.py:78.

    Cada linea del stdout que parsee como JSON se mergea en `response`; el
    resto se acumula en `log`. Es lo que permite que un script escriba prints
    de depuracion y su JSON final en el mismo stdout.
    """
    log = ''
    response = {}
    if isinstance(output, str):
        for line in output.split('\n'):
            try:
                response.update(json.loads(line))
            except Exception:
                log += str(line)
                if str(line).find('\n') < 0:
                    log += '\n'
    return response, log


def _load_dirty_json(dirty):
    """Port de backend/base/utils.py:1515: JSON escrito con comillas simples
    y True/False de Python."""
    for regex, sub in (
        (r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'),
        (r" False([, \}\]])", r' false\1'),
        (r" True([, \}\]])", r' true\1'),
    ):
        dirty = re.sub(regex, sub, dirty)
    return json.loads(dirty)


def get_exception_error(error):
    """Port de backend/scripts/tasks.py:133.

    LKFException (linkaform_api/lkf_object.py:83) termina como
    `Exception: {"exception": {...}}` al final del traceback. Se extrae ese
    JSON para que el front reciba el objeto y no el traceback completo. Si no
    se puede parsear, se devuelve el stderr tal cual, que es lo que acaba
    haciendo el back.
    """
    if not error:
        return error
    match = re.search('Exception: ', error)
    if not match:
        return error
    tail = error[match.end():]
    try:
        return json.loads(tail)
    except Exception:
        pass
    try:
        return _load_dirty_json(tail)
    except Exception:
        return error
