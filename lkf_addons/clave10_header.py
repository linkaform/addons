# coding: utf-8
'''
Marca con los headers X-Clave10-Script-Name (nombre del script) y
X-Clave10-Script-Option (opcion, si trae) cada peticion HTTP que hace un
script de una cuenta Clave10, para que infra sepa en HAProxy que script la mando
(hoy todo llega como run_script). Se carga desde sitecustomize.py en la imagen, asi
que aplica a todo proceso Python del contenedor sin tocar los scripts.

Solo marca si la cuenta tiene 'clave10': True en el config de su account_settings.py:
addons tambien lo usan cuentas que no son Clave10.

Se parchea por peticion (requests.Session.request y couchdb.http.Session.request) y no
en session.headers, porque linkaform_api reasigna session.headers en cada llamada.
'''
import os, sys, json
import importlib.abc

HEADER_NAME = 'X-Clave10-Script-Name'
HEADER_OPTION = 'X-Clave10-Script-Option'

_value_cache = []


def _script_value():
    script = os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else 'python'
    option = ''
    try:
        payload = json.loads(sys.argv[2])
        option = (payload.get('data') or {}).get('option') or payload.get('option') or ''
    except Exception:
        pass
    return script, option


def _value():
    # El flag se revisa en cada peticion: account_settings se carga despues de
    # sitecustomize y puede haber peticiones antes de que termine de armarse el config.
    # Solo se cachea el nombre del script, que no cambia.
    try:
        from linkaform_api import settings
        if not settings.config.get('clave10'):
            return None
    except Exception:
        return None
    if not _value_cache:
        _value_cache.append(_script_value())
    return _value_cache[0]


def _with_header(headers):
    value = _value()
    if not value:
        return headers
    script, option = value
    headers = dict(headers or {})
    if not any(k.lower() == HEADER_NAME.lower() for k in headers):
        headers[HEADER_NAME] = script
        if option:
            headers[HEADER_OPTION] = option
    return headers


def _patch_requests(requests):
    _session_request_orig = requests.Session.request
    def _session_request(self, method, url, **kwargs):
        kwargs['headers'] = _with_header(kwargs.get('headers'))
        return _session_request_orig(self, method, url, **kwargs)
    requests.Session.request = _session_request


def _patch_couch(couch_http):
    _couch_request_orig = couch_http.Session.request
    def _couch_request(self, method, url, body=None, headers=None, *args, **kwargs):
        return _couch_request_orig(self, method, url, body, _with_header(headers), *args, **kwargs)
    couch_http.Session.request = _couch_request


_PATCHES = {'requests': _patch_requests, 'couchdb.http': _patch_couch}


class _PatchOnImport(importlib.abc.MetaPathFinder):
    # Parchea requests/couchdb cuando el script los importa, no antes: asi un proceso
    # que no los usa no paga su import (couchdb carga pkg_resources, que es lento).
    def find_spec(self, name, path, target=None):
        if name not in _PATCHES:
            return None
        for finder in sys.meta_path:
            if finder is self:
                continue
            spec = finder.find_spec(name, path, target) if hasattr(finder, 'find_spec') else None
            if spec and spec.loader:
                exec_module = spec.loader.exec_module
                def _exec_module(module, _exec=exec_module, _patch=_PATCHES[name]):
                    _exec(module)
                    _patch(module)
                spec.loader.exec_module = _exec_module
                return spec
        return None


def install():
    if any(isinstance(f, _PatchOnImport) for f in sys.meta_path):
        return
    for name, patch in _PATCHES.items():
        if name in sys.modules:
            patch(sys.modules[name])
    sys.meta_path.insert(0, _PatchOnImport())


install()
