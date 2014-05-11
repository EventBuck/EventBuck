#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import logging
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

from shop.handlers.event.base import BaseHandler

from shop.handlers.base_handler import asso_required, user_required, RpcBaseHandler

from shop.models.activity import Activity

from shop.shop_exceptions import EventNotFoundException



class EditEventHandler(BaseHandler):
    @asso_required
    def get(self, *args, **kargs):
        
            if not self.event:
                self.redirect(self.uri_for('createEvent'))
            
            context = self.get_template_context()
            self.render_template('create_event.html', context=context)   
            
        
            
    @user_required
    def post(self, *args, **kargs):
        
        try:

            event_key = self.edit_event()
            self.redirect(self.uri_for('showEvent', event_id=event_key.id()))
        
        except EventNotFoundException:
            raise
        except:
            raise
    
    def edit_event(self):
        if not self.event:
            raise EventNotFoundException("The event_id has not been provided")
                

        posted_data = self.getRequiredPostedData()       
        event_key = self.event.edit(**posted_data)
            
        if event_key:
            self.log_this_activity(event_key)
        return event_key        
    def get_template_context(self):
            
        context = dict()
        context['event'] = self.event.get_event_in_dict_extended()
        context['edit'] = True
        context['url_for_editEvent'] = self.uri_for('editEvent', event_id=self.event_key.id())
        context['sidebar_active'] = "createEvent"
        
        return context
    
    def log_this_activity(self, target):
        self.user.log_activity(Activity(category=3, target=target))

class RpcEditEventHandler(RpcBaseHandler, EditEventHandler): 
    @user_required
    def post(self, *args, **kargs):
        try:
            event_key = self.edit_event() 
              
            if event_key:
                self.log_this_activity(event_key)
               
                
                upload_url = blobstore.create_upload_url(self.uri_for('rpcEditEventPicture', event_id = event_key.id()))
                event_url = self.uri_for('marketUserEvents', event_id=event_key.id())
                
                self.send_success_response({'upload_url':upload_url, 'event_url':event_url})
            else:
                self.abort(500)
        except:
            raise
        
   
class RpcCreateEventImage(RpcEditEventHandler, blobstore_handlers.BlobstoreUploadHandler):
    
    @user_required
    def post(self, *args, **kargs):
        try:
            if not self.event:
                raise EventNotFoundException("The event_id has not been provided")
                

            
            upload = self.get_uploads('image')
            
        
            if upload:
                
                image = upload[0].key()
                logging.warning(image)
                logging.info(image)
                self.event.edit(image = image)
                self.send_success_response()
        except:
            self.send_failed_response()