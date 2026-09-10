# coding: utf-8
"""Indice de scripts: nombre de archivo -> ruta absoluta, por destino.

Hay un indice por contenedor: los scripts de addons viven en
/srv/scripts/addons/modules y los *_sdk.py en /srv/lkf-sanic-app/modules.

El `find` se corre DENTRO del contenedor destino a proposito: garantiza que
las rutas existen ahi, y apuntar a un contenedor de worktree no necesita
montar nada extra en el mini-back.

En produccion los scripts de la cuenta viven planos en una sola carpeta, asi
que un nombre repetido no puede pasar. Aqui viven en arbol por modulo, asi
que dos modulos pueden traer el mismo nombre: eso es un error explicito, no
una eleccion silenciosa.
"""

import asyncio
import time

import runner
import settings
from errors import ContainerError, ScriptAmbiguous, ScriptNotFound

# El find es una operacion barata; no merece el timeout de un script.
FIND_TIMEOUT = 30

# Un cache y un lock por destino. Sin el lock, N peticiones que llegan juntas
# con el indice vencido lanzarian N `find` en paralelo; con el, la primera
# construye y las demas reusan.
_cache = {t['name']: {'index': None, 'built_at': 0.0} for t in settings.TARGETS}
_locks = {t['name']: asyncio.Lock() for t in settings.TARGETS}


async def _find(target):
    """Lista los .py bajo <modules_path>/*/items/scripts/** del destino."""
    cmd = [
        'docker', 'exec', target['container'],
        'find', target['modules_path'],
        '-path', '*/items/scripts/*',
        '-name', '*.py',
    ]
    try:
        returncode, stdout, stderr = await runner.exec_async(cmd, FIND_TIMEOUT)
    except asyncio.TimeoutError:
        raise ContainerError(
            'construir el indice tardo mas de {}s en el contenedor "{}"'.format(
                FIND_TIMEOUT, target['container']))

    if returncode != 0:
        stderr = (stderr or '').strip()
        raise ContainerError(
            'no se pudieron listar los scripts del contenedor "{}": {}'.format(
                target['container'], stderr or 'returncode {}'.format(returncode)))

    return [line.strip() for line in stdout.splitlines() if line.strip()]


async def build_index(target):
    """{'script_turnos.py': ['/srv/.../script_turnos.py', ...]}"""
    index = {}
    for path in await _find(target):
        index.setdefault(path.rsplit('/', 1)[-1], []).append(path)

    duplicados = sorted(name for name, paths in index.items() if len(paths) > 1)
    print('miniback: indice [{}] construido, {} scripts en "{}"'.format(
        target['name'], len(index), target['container']))
    if duplicados:
        print('miniback: [{}] {} nombres repetidos en mas de un modulo: {}'.format(
            target['name'], len(duplicados), ', '.join(duplicados)))

    return index


async def get_index(target, force=False):
    """Indice cacheado del destino. Se reconstruye al pasar MINIBACK_INDEX_TTL."""
    cache = _cache[target['name']]

    def vencido():
        return (cache['index'] is None
                or time.time() - cache['built_at'] >= settings.INDEX_TTL)

    if not force and not vencido():
        return cache['index']

    async with _locks[target['name']]:
        # Otra peticion pudo haberlo reconstruido mientras esperabamos el lock.
        if force or vencido():
            cache['index'] = await build_index(target)
            cache['built_at'] = time.time()

    return cache['index']


async def resolve(script_name):
    """(ruta, destino) del script. El destino sale del nombre, sin fallback:
    un *_sdk.py que no este en el contenedor de Sanic es ScriptNotFound, no
    se busca en addons."""
    target = settings.target_for(script_name)
    index = await get_index(target)
    matches = index.get(script_name, [])
    if not matches:
        raise ScriptNotFound(script_name, target)
    if len(matches) > 1:
        raise ScriptAmbiguous(script_name, sorted(matches))
    return matches[0], target
