#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 21 sept. 2013

@author: Aristote Diasonama
'''
from market.handlers.main import MainHandler

class FacebookInviteHandler(MainHandler):
    def get(self):
        context = self.get_index_context()
                
        context['events'] = context['events'][:15]
        
        self.render_template('facebook_canvas.html', context)
    def post(self):
        context = self.get_index_context()
                
        context['events'] = context['events'][:15]
        
        self.render_template('facebook_canvas.html', context)