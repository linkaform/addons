# -*- coding: utf-8 -*-

from linkaform_api import base


class Accesos(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        #--Variables Forms
        self.FORM_ALTA_COLABORADORES = self.lkm.form_id('alta_de_colaboradores_visitantes','id')
        self.FORM_ALTA_EQUIPOS = self.lkm.form_id('alta_de_equipos','id')
        self.FORM_ALTA_VEHICULOS = self.lkm.form_id('alta_de_vehiculos','id')
        self.FORM_BITACORA = self.lkm.form_id('bitacora','id')
        self.FORM_LOCKER = self.lkm.form_id('locker','id')
        self.FORM_PASE_DE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        self.FORM_REGISTRO_PERMISOS = self.lkm.form_id('registro_de_permisos','id')

        #----Dic Fields Forms
        self.f = {
            'key':'form_field_ObjectId()'
        }
