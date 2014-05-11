#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 30 ao�t 2013

@author: Aristote Diasonama
'''

from shop.handlers.base_handler import RpcBaseHandler
from shop.models.report import Report
from market.market_exceptions import RpcMarketException
from shop.handlers.base_handler import user_required
from google.appengine.ext import ndb

class RpcReportingHandler(RpcBaseHandler):
    @user_required
    def post(self):
        try:
            event_key_urlsafe = self.request.get('event_key')
            event_key = ndb.Key(urlsafe = event_key_urlsafe)
            if not self.file_a_report(event_key):
                raise RpcMarketException(msg="Unable to save the message")
            self.send_success_response()
        except RpcMarketException as e:
            self.send_failed_response(e)
            
    
    def file_a_report(self, event_key):
        report_key =  Report.is_report_exist(event_key)
        if report_key:
            return report_key
            
        else :
            return Report.create_report(self.user.key, event_key)
        
