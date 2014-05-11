#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 26 juil. 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb

from .base import BaseHandler
from market.handlers.base import student_required
from shop.shop_exceptions import EventNotFoundException
from shop.handlers.base_handler import RpcBaseHandler
from shop.models.activity import Activity
from market.handlers.main import RpcMainGetEvents
from market.lib.attendance import AttendanceManager
from market.lib.event import EventManager


    
class ShowAttendingHandler(BaseHandler):
    @student_required
    def get(self):
        context = self.get_template_context()
        context['events'] = context['events'][:15]
        context['attending'] = True
        self.render_template('show_many_events.html', context)
        
    def get_template_context(self):
        context = dict()
        context['left_sidebar'] = 'attending'
        context['events'] = EventManager.get_events_attending(self.user_info['user_id'])
        return context

class RpcAttendingGetEvents(ShowAttendingHandler, RpcMainGetEvents):
    @student_required
    def get(self, *args, **kargs):
        filter_key = self.request.get('filter_key')
        sort_order = self.request.get('sort_order')
        tab = self.request.route_kwargs.get('page')
        events = EventManager.get_events_attending(self.user_info['user_id'], 
                                                        category=tab, 
                                                        filtered_by=filter_key, 
                                                        ordered_by=sort_order)
            
        self.prepare_and_serve_events(events)

class RpcAttendEvent(BaseHandler, RpcBaseHandler):
    
    @student_required
    def post(self):
        try:
            if self.request.get('attend_key'):
                attendance_key = ndb.Key(urlsafe = self.request.get('attend_key'))
                AttendanceManager.cancel_attendance(attendance_key, 
                                                    self.event, 
                                                    self.user_info['user_id'])
                self.log_this_activity()
                self.send_success_response()
            else:
                     
                if not self.user.is_attending_event(self.event):
                   
                    attending_key = self.attend_event()
                    self.log_this_activity()
                    self.send_success_response(attending_key)
                else:
                    self.send_success_response()
        
        except EventNotFoundException as e:
            self.send_failed_response(e)
    
    def attend_event(self):
        if not self.event:
            raise EventNotFoundException
        return EventManager.attend_event(self.user_info['user_id'], event_key = self.event)
 
   
    def log_this_activity(self):
        if self.request.get('attend_key'):
            self.user.log_activity(Activity(category=9, target=self.event))
        else:   
            self.user.log_activity(Activity(category=8, target=self.event))
                   
  


    