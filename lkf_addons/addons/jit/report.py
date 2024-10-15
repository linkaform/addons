# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from linkaform_api import base

from .app import JIT

print('carga base')

class Reports(base.LKF_Report):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)



    def test(self):
        print('test')