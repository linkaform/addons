# -*- coding: utf-8 -*-
import sys, simplejson

from linkaform_api import settings
from linkaform_api import base


class Employee(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings
        self.EMPLOYEE = self.lkm.catalog_id('employee')
        self.EMPLOYEE_ID = self.EMPLOYEE.get('id')
        self.EMPLOYEE_OBJ_ID = self.EMPLOYEE.get('obj_id')
        self.TEAM = self.lkm.catalog_id('teams')
        self.TEAM_ID = self.TEAM.get('id')
        self.TEAM_OBJ_ID = self.TEAM.get('obj_id')
        self.f.update( {
            'team_name':'62c5ff0162a70c261328845d',
            }
            )

    def una_funcion_employee(self):
        return True
