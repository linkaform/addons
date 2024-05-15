# -*- coding: utf-8 -*-

from linkaform_api import base


class Base(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #use self.lkm.catalog_id() to get catalog id
        self.f = {
            'key':'form_field_ObjectId()'
        }
