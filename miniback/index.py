# coding: utf-8
"""Indice de scripts: nombre de archivo -> ruta absoluta.

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

_cache = {'index': None, 'built_at': 0.0}
# Sin este lock, 10 peticiones que llegan juntas con el indice vencido
# lanzarian 10 `find` en paralelo. Con el, el primero construye y los otros
# nueve esperan y reusan.
_lock = asyncio.Lock()


async def _find():
    """Lista los .py bajo modules/*/items/scripts/** del contenedor destino."""
    cmd = [
        'docker', 'exec', settings.CONTAINER,
        'find', settings.MODULES_PATH,
        '-path', '*/items/scripts/*',
        '-name', '*.py',
    ]
    try:
        returncode, stdout, stderr = await runner.exec_async(cmd, FIND_TIMEOUT)
    except asyncio.TimeoutError:
        raise ContainerError(
            'construir el indice tardo mas de {}s en el contenedor "{}"'.format(
                FIND_TIMEOUT, settings.CONTAINER))

    if returncode != 0:
        stderr = (stderr or '').strip()
        raise ContainerError(
            'no se pudieron listar los scripts del contenedor "{}": {}'.format(
                settings.CONTAINER, stderr or 'returncode {}'.format(returncode)))

    return [line.strip() for line in stdout.splitlines() if line.strip()]


async def build_index():
    """{'script_turnos.py': ['/srv/.../script_turnos.py', ...]}"""
    index = {}
    for path in await _find():
        index.setdefault(path.rsplit('/', 1)[-1], []).append(path)

    duplicados = sorted(name for name, paths in index.items() if len(paths) > 1)
    print('miniback: indice construido, {} scripts en "{}"'.format(
        len(index), settings.CONTAINER))
    if duplicados:
        print('miniback: {} nombres repetidos en mas de un modulo: {}'.format(
            len(duplicados), ', '.join(duplicados)))

    return index


async def get_index(force=False):
    """Indice cacheado. Se reconstruye cuando pasa MINIBACK_INDEX_TTL."""
    def vencido():
        return (_cache['index'] is None
                or time.time() - _cache['built_at'] >= settings.INDEX_TTL)

    if not force and not vencido():
        return _cache['index']

    async with _lock:
        # Otra peticion pudo haberlo reconstruido mientras esperabamos el lock.
        if force or vencido():
            _cache['index'] = await build_index()
            _cache['built_at'] = time.time()

    return _cache['index']


async def resolve(script_name):
    """Ruta absoluta del script dentro del contenedor destino."""
    index = await get_index()
    matches = index.get(script_name, [])
    if not matches:
        raise ScriptNotFound(script_name)
    if len(matches) > 1:
        raise ScriptAmbiguous(script_name, sorted(matches))
    return matches[0]
