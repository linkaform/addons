# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo proporciona las funcionalidades modulares de LinkaForm. Con estas funcionalidades, 
podrás utilizar la plataforma LinkaForm de manera modular, como un Backend as a Service (BaaS).

Licencia BSD
Copyright (c) 2024 Infosync / LinkaForm.  
Todos los derechos reservados.

Se permite la redistribución y el uso en formas de código fuente y binario, con o sin modificaciones, siempre que se cumplan las siguientes condiciones:

1. Se debe conservar el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en las redistribuciones del código fuente.
2. Se debe reproducir el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en la documentación y/u otros materiales proporcionados con las distribuciones en formato binario.
3. Ni el nombre del Infosync ni los nombres de sus colaboradores pueden ser utilizados para respaldar o promocionar productos derivados de este software sin permiso específico previo por escrito.


Propósito
El propósito de este archivo es ser auto documentable y adaptable, facilitando la reutilización 
de gran parte del código en otros módulos simplemente copiando y pegando las secciones necesarias.

Instrucciones
1. Al copiar secciones de código, asegúrate de incluir la documentación correspondiente.
2. Al crear un nuevo archivo o módulo, copia las instrucciones y las generales aplicables a cada archivo.
3. Puedes basarte en la carpeta `_templates` o sus archivos para crear nuevos módulos.
'''

### Archivo de Modulo ###
'''
Este archivo define las funciones generales del módulo. Por conveniencia, se nombra `app.py`. 

Si tienes más de una aplicación, puedes:
    a. Crear una carpeta llamada `app`.
    b. Guardar los archivos a nivel raíz.
    c. Nombrar los archivos por conveniencia o estándar: `app_utils.py`, `utils.py`, `xxx_utils.py`.
'''

# Importaciones necesarias
from lkf_addons.addons.base.app import Base

### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class WorkflowLogs(Base):
    
    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)


    def _get_date_query(self, date_from, date_to):
        """
        Construye filtro de fechas sobre created_at (Date).
        Acepta strings 'YYYY-MM-DD'. Devuelve dict parcial para $match.
        """
        q = {}
        if date_from:
            if isinstance(date_from, str):
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
            q.setdefault("created_at", {})["$gte"] = date_from
        if date_to:
            if isinstance(date_to, str):
                # incluir todo el día -> fin: 23:59:59
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
                # sumamos 1 día, y el operador < siguiente día
                from datetime import timedelta
                date_to = date_to + timedelta(days=1)
            q.setdefault("created_at", {})["$lt"] = date_to
        return q

    def query_workflow_logs(self, date_from=None, date_to=None, form_id=None, only_failed=True, limit=100):
        """
        Ejecuta el aggregation sobre workflow_log.
        """
        # --- Colección de workflow logs

        # --- Match base
        match_query = {}
        # Opcional: filtrar por form_id
        if form_id:
            try:
                # permitir int o str
                form_id = int(form_id)
            except Exception:
                pass
            match_query.update({"form_id": form_id})

        # Fechas
        date_q = self._get_date_query(date_from, date_to)
        if date_q:
            match_query.update(date_q)

        # Solo fallidos (workflow_sucess != true o no existe)
        if only_failed:
            match_query.update({
                "$or": [
                    {"workflow_sucess": {"$ne": True}},
                    {"workflow_sucess": {"$exists": False}}
                ]
            })

        pipeline = [
            {"$match": match_query},
            {
                "$project": {
                    "_id": 0,
                    "folio": {"$ifNull": ["$workflow_record_folio", "$folio"]},
                    "record_status": 1,
                    "workflow_rule_name": 1,
                    "workflow_sucess": 1,
                    "workflow_rule": 1,
                    "form_id": 1,
                    "name": 1,
                    "user_id": 1,
                    "workflow_response_content": 1,
                    # fecha legible
                    "created_at_str": {
                        "$dateToString": {"date": "$created_at", "format": "%Y-%m-%d %H:%M:%S", "timezone": "America/Monterrey"}
                    },
                    # link directo al record
                    "link": {
                        "$concat": [LINKA_RECORD_URL, {"$toString": "$record_id"}]
                    }
                }
            },
            {"$sort": {"created_at_str": -1}},
        ]

        if limit and isinstance(limit, int) and limit > 0:
            pipeline.append({"$limit": limit})
        print('pipeline=', simplejson.dumps(pipeline, indent=4))
        res = self.cr_wkf.aggregate(pipeline)
        return [x for x in res]
