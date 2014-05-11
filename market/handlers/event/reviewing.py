#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 6 janv. 2014

@author: didia
'''

from shop.handlers.base_handler import RpcBaseHandler
from market.handlers.main import RpcMainGetEvents
from market.lib import event_review
from market.lib.attendance import AttendanceManager
from market.lib.event import EventManager
from market.market_exceptions import RpcMarketException
from market.handlers.base import student_required
from google.appengine.ext import ndb
from .base import BaseHandler

def participant_required(handler):
    
    def check_participation(self, *args, **kargs):
        event_key = self.request.get('event_key')
        if AttendanceManager.is_user_attending_event(event_key, self.user_info['user_id']):
            return handler(self, *args, **kargs)
        else:
            self.abort(404)


    
class ShowReviewingHandler(BaseHandler):
    @student_required
    def get(self):
        context = self.get_template_context()
        context['events'] = context['events'][:15]
        self.render_template('show_many_events.html', context)
        
    def get_template_context(self):
        context = dict()
        context['left_sidebar'] = 'reviewing'
        context['events'] = EventManager.get_events_reviewing(self.user_info['user_id'])
        return context

class RpcReviewingGetEvents(ShowReviewingHandler, RpcMainGetEvents):
    @student_required
    def get(self, *args, **kargs):
        filter_key = self.request.get('filter_key')
        sort_order = self.request.get('sort_order')
        tab = self.request.route_kwargs.get('page')
        events = EventManager.get_events_reviewing(self.user_info['user_id'], 
                                                        category=tab, 
                                                        filtered_by=filter_key, 
                                                        ordered_by=sort_order)
            
        self.prepare_and_serve_events(events)        

class RpcReviewingHandler(RpcBaseHandler):
    @student_required
    def post(self):
        try:
            event_key_urlsafe = self.request.get('event_key')
            score = int(self.request.get('score'))
            if score < 1 or score > 5:
                raise RpcMarketException(msg="Unable to save the message")
            
            self.review_event(event_key_urlsafe, score)
            
            self.send_success_response()
        except RpcMarketException as e:
            self.send_failed_response(e)
            
    #@participant_required
    def review_event(self, event_key, score):
        return event_review.review_event(event_key, self.user_info['user_id'], score)
        
