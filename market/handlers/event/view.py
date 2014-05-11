#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''
from webapp2 import cached_property
import memcache
from concurrent.futures.thread import ThreadPoolExecutor
from google.appengine.ext import ndb

from shop.models.event import Event
from shop.shop_exceptions import EventNotFoundException
from market.lib.event import EventManager
from market.lib import pageview_tracker
from market.lib import event_stat_tracker as stat_tracker
from market.handlers.event.user_events import ShowEventHandler

      
def get_context(event_key, user_id, url):
    
    if user_id:
        event = EventManager.get_marked_event(event_key, user_id)
    else:
        event = EventManager.get_event(event_key)
    if not event:
        return None
    context = {}
    context['event'] = event
    
    event_key = event_key.urlsafe()
    
    if user_id and event['is_active'] and event['reviewing'] and event['seller_id'] != user_id:
        context['event']['can_review'] = True
    reviews = stat_tracker.get_reviews(event_key)

    if reviews:
        context['event']['rating'] = reviews.get('av_score', 0)
        context['event']['reviewers_number'] = len(reviews['reviews'].keys())
        if user_id in reviews['reviews'].keys():
            context['event']['has_user_reviewed'] = True
            context['event']['user_score'] = reviews['reviews'].get(user_id, 0)

          
    boys_number = stat_tracker.get_number_of_boys(event_key)
    girls_number = stat_tracker.get_number_of_girls(event_key)
      
    event['attendees_number'] =  boys_number + girls_number 
    if event['attendees_number'] > 0:
        event['girls_ratio'] = (girls_number * 100.0)/event['attendees_number']
       
    
    return context
          
def track_page_view(page_key, ip_adress, user_id): 
    print("Page vues: ", pageview_tracker.get_page_views(page_key))
    pageview_tracker.track_visit(page_key, ip_adress, user_id)


class ViewEventHandler(ShowEventHandler):
    
    
    def get(self, *args, **kargs):
        
        try:
            
            if self.user and EventManager.is_user_owner(self.user_info['user_id'], 
                                          self._get_event_key) and not self.request.get('view_as'):
                ShowEventHandler.get(self)
            else:
                
                user_id = self.user_info['user_id'] if self.user else None
            
                with ThreadPoolExecutor(max_workers=2) as e:
                    if EventManager.is_event_upcoming(self._get_event_key) and not self.request.get('view_as'):
                        page_key = self._get_event_key.urlsafe()
                        ip_adress = self.request.remote_addr
                    
                        e.submit(track_page_view, page_key, ip_adress, user_id)
    
                    context = e.submit(get_context,self._get_event_key, user_id).result()
        
                    if context.get('event') is None:
                        raise EventNotFoundException
            
                self.render_template('event.html', context)
            
        except EventNotFoundException:
            raise
    
    @cached_property
    def _get_event_key(self):
        user_key = ndb.Key(self.user_model, int(self.request.route_kwargs.get('user_id')))
        event_key = ndb.Key(Event, int(self.request.route_kwargs.get('event_id')), parent=user_key)
        return event_key
    
