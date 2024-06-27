# -*- coding: utf-8 -*-
import sys, simplejson, math
from datetime import timedelta, datetime

from linkaform_api import settings
from account_settings import *

print('inicia....')
from stock_report import Reports

    
print('ESTE....', Reports)

if __name__ == '__main__':
    report_obj = Reports(settings, sys_argv=sys.argv, use_api=True)
    report_obj.console_run()
    #getFilters
    print('data',report_obj.data.get('data'))
    option = report_obj.data.get('data').get("option",0)
    product_code = report_obj.data.get('data').get("product_code")
    print('option',option)
    print('product_code',product_code)
    if option == 'getFilters': 
        filters = ['products','warehouse']
        filter_data = report_obj.get_report_filters(filters)
    elif option =='getLotNumber':
        filters = ['inventory',]
        filter_data = report_obj.get_report_filters(filters, product_code=product_code)
    else:
        data, actuals = report_obj.get_product_kardex()
        report_obj.json['firstElement'] = {'data':[]}
        report_obj.json['secondElement'] = {'data':data}
        report_obj.json['actuals'] = actuals

    sys.stdout.write(simplejson.dumps(report_obj.report_print()))

