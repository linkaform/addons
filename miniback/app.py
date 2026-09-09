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
    # Se resuelve una sola vez, para que armar script_args no cueste un
    # `docker inspect` por peticion.
    await runner.docker_image()


@app.after_server_stop
async def cerrar_cliente(app, loop):
    await app.ctx.http.aclose()


@app.get('/api/health')
async def health(request):
    body = {
        'ok': True,
        'container': settings.CONTAINER,
        'account_id': settings.ACCOUNT_ID,
    }
    try:
        body['scripts'] = len(await index.get_index())
    except ContainerError as e:
        # El mini-back esta vivo; el que no responde es el contenedor de addons.
        body['ok'] = False
        body['scripts'] = 0
        body['error'] = str(e)
    return json_response(body)


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
        script_path = await index.resolve(script_name)
    except ScriptNotFound:
        return json_response({
            'code': 11,
            'error': 'The script does not exist.',
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
        return json_response({
            'code': 12, 'error': str(e), 'success': False}, status=400)

    if runner._cache['docker_image'] is None:
        # El contenedor pudo haber arrancado despues del mini-back.
        await runner.docker_image()

    args = runner.build_args(body, request.headers.get('Authorization'), script_path)

    try:
        returncode, stdout, stderr = await runner.run(script_path, args)
    except (ContainerError, ScriptTimeout) as e:
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
    print('miniback: contenedor destino = {}'.format(settings.CONTAINER))
    print('miniback: account_id por default = {}'.format(settings.ACCOUNT_ID))
    app.run(
        host='0.0.0.0',
        port=settings.LISTEN_PORT,
        single_process=True,
        access_log=True,
    )
