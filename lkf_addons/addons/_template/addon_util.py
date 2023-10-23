# -*- coding: utf-8 -*-

from linkaform_api import base


class ModuleName(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None):
        base.LKF_Base.__init__(self, settings)
        #use self.lkm.catalog_id() to get catalog id
        self.f = {
            'key':'form_field_ObjectId()'
        }
