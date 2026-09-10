# coding: utf-8
"""Mini-back local: simula la parte del backend de LinkaForm que corre
scripts de addons dentro del contenedor de la cuenta.

No reemplaza a infosync-api. Solo existe para desarrollo local.
"""

import httpx
from sanic import Sanic
from sanic.response import empty
from sanic.response import json as json_response
from sanic.response import raw

import index
import runner
import settings
from errors import ContainerError, ScriptAmbiguous, ScriptNotFound, ScriptTimeout

app = Sanic('miniback')

# CORS abierto: el front corre en localhost:3000 y esto en localhost:8000.
# Es una herramienta local, nunca se publica.
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Max-Age': '86400',
}


@app.on_request
async def preflight(request):
    """El navegador manda OPTIONS antes de cada POST con Authorization."""
    if request.method == 'OPTIONS':
        return empty(status=204, headers=CORS_HEADERS)


@app.on_response
async def cors(request, response):
    response.headers.update(CORS_HEADERS)


def get_body(request):
    """El body de la peticion, venga por POST o por GET.

    El back real acepta las dos (script_resource.py:520-523): en GET cada
    query param es una llave del body.
    """
    if request.method == 'GET':
        return {k: v[0] for k, v in request.args.items()}
    try:
        return request.json or {}
    except Exception:
        return None


@app.before_server_start
async def abrir_cliente(app, loop):
    app.ctx.http = httpx.AsyncClient(timeout=30.0)
    # Se resuelven una sola vez, para que armar script_args no cueste un
    # `docker inspect` por peticion. Si un contenedor esta abajo no pasa nada:
    # se reintenta en la peticion que lo necesite.
    for target in settings.TARGETS:
        await runner.docker_image(target)


@app.after_server_stop
async def cerrar_cliente(app, loop):
    await app.ctx.http.aclose()


@app.get('/api/health')
async def health(request):
    destinos = []
    todo_ok = True
    for target in settings.TARGETS:
        destino = {
            'name': target['name'],
            'container': target['container'],
            'runs': 'todo lo demas' if target['name'] == 'addons'
                    else '*{}'.format(settings.SDK_SUFFIX),
        }
        try:
            destino['scripts'] = len(await index.get_index(target))
            destino['ok'] = True
        except ContainerError as e:
            # El mini-back esta vivo; el que no responde es la dependencia.
            destino['ok'] = False
            destino['scripts'] = 0
            destino['error'] = str(e)
            todo_ok = False
        destinos.append(destino)

    return json_response({
        'ok': todo_ok,
        'account_id': settings.ACCOUNT_ID,
        'targets': destinos,
    })


@app.route('/api/infosync/scripts/run/', methods=['POST', 'GET', 'OPTIONS'],
           strict_slashes=False)
async def scripts_run(request):
    body = get_body(request)
    if body is None:
        return json_response(
            {'error': 'Incorrect format in request body.'}, status=400)

    script_name = body.get('script_name')
    if not script_name:
        # Mismo mensaje que script_resource.py:670-674.
        return json_response({'error': 'Missing params.', 'success': False}, status=400)

    try:
        script_path, target = await index.resolve(script_name)
    except ScriptNotFound as e:
        contenedor = e.target['container'] if e.target else '?'
        return json_response({
            'code': 11,
            'error': 'The script does not exist.',
            'detail': '{} no esta en el indice de "{}"'.format(
                script_name, contenedor),
            'container': contenedor,
            'success': False,
        }, status=404)
    except ScriptAmbiguous as e:
        return json_response({
            'code': 20,
            'error': str(e),
            'matches': e.matches,
            'success': False,
        }, status=400)
    except ContainerError as e:
        # La dependencia esta caida: no es un error de la peticion.
        return json_response({
            'code': 12, 'error': str(e), 'success': False}, status=503)

    if not runner._cache['docker_image'].get(target['container']):
        # El contenedor pudo haber arrancado despues del mini-back.
        await runner.docker_image(target)

    args = runner.build_args(
        body, request.headers.get('Authorization'), script_path, target)

    try:
        returncode, stdout, stderr = await runner.run(target, script_path, args)
    except ContainerError as e:
        # La dependencia esta caida: no es un error de la peticion.
        return json_response({
            'code': 12,
            'error': str(e),
            'container': target['container'],
            'response': {},
            'log': '',
            'success': False,
        }, status=503)
    except ScriptTimeout as e:
        # Aqui si fallo el script: se colgo.
        return json_response({
            'code': 12,
            'error': str(e),
            'response': {},
            'log': '',
            'success': False,
        }, status=400)

    response, log = runner.format_output(stdout)

    if returncode != 0 or 'Exception: ' in stderr:
        return json_response({
            'code': 12,
            'error': runner.get_exception_error(stderr),
            'response': response,
            'log': log,
            'success': False,
        }, status=400)

    return json_response({'response': response, 'log': log, 'success': True})


@app.route('/api/infosync/user_admin/login/', methods=['POST', 'OPTIONS'],
           strict_slashes=False)
async def login(request):
    """Proxy transparente a LinkaForm.

    El login no se simula: se reenvia a produccion para que el JWT que
    devuelve sea real y sirva para que los scripts peguen a la API de verdad.
    """
    url = '{}/api/infosync/user_admin/login/'.format(settings.UPSTREAM)
    headers = {}
    for name in ('content-type', 'authorization', 'accept', 'accept-language'):
        if name in request.headers:
            headers[name] = request.headers[name]

    print('miniback: login -> {}'.format(url))
    try:
        upstream = await request.app.ctx.http.post(
            url, content=request.body, headers=headers)
    except httpx.HTTPError as e:
        print('miniback: el login contra {} fallo: {}'.format(settings.UPSTREAM, e))
        return json_response({
            'error': 'No se pudo contactar {}: {}'.format(settings.UPSTREAM, e),
            'success': False,
        }, status=502)

    print('miniback: login <- {}'.format(upstream.status_code))
    return raw(
        upstream.content,
        status=upstream.status_code,
        content_type=upstream.headers.get('content-type', 'application/json'),
    )


if __name__ == '__main__':
    for target in settings.TARGETS:
        print('miniback: destino [{}] -> contenedor "{}" ({})'.format(
            target['name'], target['container'],
            'todo lo demas' if target['name'] == 'addons'
            else '*{}'.format(settings.SDK_SUFFIX)))
    print('miniback: account_id por default = {}'.format(settings.ACCOUNT_ID))
    app.run(
        host='0.0.0.0',
        port=settings.LISTEN_PORT,
        single_process=True,
        access_log=True,
    )
