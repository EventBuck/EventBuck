#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import blobstore
from shop.handlers.event.base import BaseHandler

from shop.handlers.base_handler import asso_required, user_required, RpcBaseHandler

from shop.models.activity import Activity




class CreateEventHandler(BaseHandler):
    @asso_required
    def get(self):
        
        self.render_template('create_event.html', {'sidebar_active':"createEvent"})
        
    @user_required
    def post(self):
        try:
            
            posted_data = self.getRequiredPostedData()
            
            
            if self.request.get('type') == 'paid':
                event_key = self.create_paid_event(**posted_data)
            else:
                event_key = self.create_free_event(**posted_data)
            
        
            if event_key:
                self.logThisActivity(event_key)
            self.event_key = event_key
            self.redirect(self.uri_for('showEvent', event_id=event_key.id()))
        except:
            raise
    
    def create_paid_event(self, **posted_data):
        return self.user.create_paid_event(**posted_data)
    
    def create_free_event(self, **posted_data):
        return self.user.create_free_event(**posted_data)
        
    def logThisActivity(self, target):
        self.user.log_activity(Activity(category=1, target=target))   

class RpcCreateEventHandler(RpcBaseHandler, CreateEventHandler):
    
    @user_required
    def post(self, *args, **kargs):
        try:
            posted_data = self.getRequiredPostedData() 
            if self.request.get('type') == 'paid':
                event_key = self.create_paid_event(**posted_data)
            else:
                event_key = self.create_free_event(**posted_data)
            if event_key:
                self.logThisActivity(event_key)
                
                upload_url = blobstore.create_upload_url(self.uri_for('rpcEditEventPicture', event_id = event_key.id()))
                event_url = self.uri_for('marketUserEvents', event_id=event_key.id())
                
                self.send_success_response({'upload_url':upload_url, 'event_url':event_url})
            else:
                self.abort(500)
        except Exception :
            raise