#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 15 juil. 2013

@author: Aristote Diasonama
'''

from django.utils import simplejson

from market.handlers.main import MainHandler

class RpcGetHandler(MainHandler):
    def get(self):
        up_coming_events = self.get_upcoming_events()
        self.response.out.write(simplejson.dumps(up_coming_events))
        