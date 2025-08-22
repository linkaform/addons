# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from .app import WorkflowLogs

from linkaform_api import base


class Reports(base.LKF_Report, WorkflowLogs):


    def query_workflow_logs(self, date_from=None, date_to=None, form_id=None, only_failed=True, limit=1000):
        """
        Ejecuta el aggregation sobre workflow_log.
        """
        # --- Colección de workflow logs
        cl = self.db['workflow_log']  # <-- ajusta aquí si tu alias/colección difiere

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
                    "form_id": 1,
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

        res = cl.aggregate(pipeline)
        return [x for x in res]