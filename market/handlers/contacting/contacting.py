#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 29 ao�t 2013

@author: Aristote Diasonama
'''

from shop.handlers.base_handler import RpcBaseHandler
from shop.models.message import ContactMessage
from market.market_exceptions import RpcMarketException

class RpcContactingHandler(RpcBaseHandler):
    def post(self):
        try:
            message_data= self.get_required_posted_data()
            if self.user:
                user_key = self.user.key
            else:
                user_key = None
        
            message_key = self.create_message(user_key, message_data)
            if message_key:
                self.send_success_response()
            else:
                raise RpcMarketException(msg="Unable to save the message")
        
        except RpcMarketException as error:
            self.send_failed_response(error)
    
    
    def create_message(self, user_key, message_data):
        return ContactMessage.create_message(user_key, **message_data)
    
                
        
    def get_required_posted_data(self):
        list_of_datas_to_clean = ['name', 'email', 'subject', 'message', 'type']
        cleaned_data = self.cleanPostedData(list_of_datas_to_clean)
        return cleaned_data