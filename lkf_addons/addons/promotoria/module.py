# -*- coding: utf-8 -*-

from linkaform_api import base


class Promotoria(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #use self.lkm.catalog_id() to get catalog id
        self.f.update( {
            'key':'form_field_ObjectId()'
        })
