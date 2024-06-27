# -*- coding: utf-8 -*-
import sys, simplejson, math
from datetime import timedelta, datetime


from lab_stock_report import Reports

from account_settings import *

if __name__ == '__main__':

    report_obj = Reports(settings, sys_argv=sys.argv)
    report_obj.console_run()
    product_code = str(report_obj.answers.get('61ef32bcdf0ec2ba73dec33c',{}).get('61ef32bcdf0ec2ba73dec33d',''))
    lot_number = int(report_obj.answers.get('620a9ee0a449b98114f61d77',0))
    # report_obj.console_run()
    #answers = {"61ef32bcdf0ec2ba73dec33c":{"61ef32bcdf0ec2ba73dec33d":"LNAFP"},"620a9ee0a449b98114f61d77":202350}
    answers = {"61ef32bcdf0ec2ba73dec33c":{"61ef32bcdf0ec2ba73dec33d":product_code},"620a9ee0a449b98114f61d77":lot_number}

    report_obj.data = {'data':
        {
        'product_code': answers.get(report_obj.CATALOG_PRODUCT_RECIPE_OBJ_ID,{} ).get(report_obj.f['product_code']),
        'lot_number': answers.get(report_obj.f.get('product_lot'))
        }
    }
    data, actuals = report_obj.get_product_kardex()
    print(">>>>>>")
    actuals = str(actuals)
    res = {'response':data, 'product_code':product_code, 'lot_number': lot_number, 'actuals':actuals}
    sys.stdout.write(simplejson.dumps(res))

