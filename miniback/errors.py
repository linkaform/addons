# coding: utf-8
"""Errores del mini-back, compartidos por index.py y runner.py.

Todos llevan un mensaje presentable: terminan en el `error` de la respuesta
HTTP, no en un stacktrace.
"""


class MinibackError(Exception):
    """Error con mensaje presentable para quien llamo al endpoint."""


class ContainerError(MinibackError):
    """El contenedor de addons no existe, no corre, o no se pudo hablar con el."""


class ScriptNotFound(MinibackError):
    """El script_name no esta en el indice de su destino."""

    def __init__(self, script_name, target=None):
        self.script_name = script_name
        self.target = target
        super().__init__(script_name)


class ScriptTimeout(MinibackError):
    """El script paso de MINIBACK_TIMEOUT segundos."""


class ScriptAmbiguous(MinibackError):
    """El mismo nombre de archivo aparece en mas de un modulo."""

    def __init__(self, script_name, matches):
        self.script_name = script_name
        self.matches = matches
        super().__init__('script_name ambiguo: {} coincidencias'.format(len(matches)))
