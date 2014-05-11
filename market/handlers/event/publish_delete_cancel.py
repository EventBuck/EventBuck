#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 22 juin 2013

@author: Aristote Diasonama
'''

import memcache
from shop.handlers.event.base import BaseHandler
from shop.handlers.base_handler import RpcBaseHandler, user_required
from shop.shop_exceptions import EventNotFoundException, InvalidEventError
from shop.shop_exceptions import EventInMarketError
from shop.shop_exceptions import UserNotAllowed
from shop.models.activity import Activity
from market.lib.event import EventManager
from google.appengine.api import taskqueue


class RpcPublishEventHandler(RpcBaseHandler, BaseHandler):
    
    @user_required
    def post(self, *args, **kargs):
        try:
            event_id = self.request.get('event_id') or self.request.route_kwargs.get('event_id')
            published = self.publish_event(int(event_id))
            if published:
                self.log_this_activity()
                self.send_success_response()
                task = taskqueue.add(url=self.uri_for('marketUpdate'))
                
        
        except EventNotFoundException as e:
            self.send_failed_response(e)
        
        except InvalidEventError as e:
            self.send_failed_response(e) 
        except UserNotAllowed:
            if self.user.type == 'student':
                email = self.user.u_email
            else:
                email = self.user.email
                
            self.send_failed_response(UserNotAllowed(email))
    
    def publish_event(self, event_id):
        if not self.user.verified:
            raise UserNotAllowed('The user can\'t publish because he is not verified')
        
        return EventManager.publish_event(event_id, self.user)
    
    def log_this_activity(self):
        self.user.log_activity(Activity(category=5, target=self.event_key))
        if self.user.type == 'student':
            self.user.log_activity(Activity(category=8, target=self.event_key))
                   
        
    

class RpcDeleteEventHandler(RpcBaseHandler, BaseHandler):
    @user_required
    def post(self, *args, **kargs):
        try:
            self.delete_event()
            self.send_success_response()
        except EventNotFoundException:
            raise
            
        except EventInMarketError:
            raise
    
    def delete_event(self):
        if not self.event:
            raise EventNotFoundException
        if self.event.published:
            self.user.events_published -= 1
        self.event.delete_event()
        memcache.delete_event(self.event.key.urlsafe())
    def log_this_activity(self):
        self.user.log_activity(Activity(category=7))
         


      
            
        