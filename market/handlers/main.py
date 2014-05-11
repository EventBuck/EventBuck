#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 8 juil. 2013

@author: Aristote Diasonama
'''


from .base import BaseHandler
from market.lib.event import EventManager



from shop.handlers.base_handler import RpcBaseHandler


class MainHandler(BaseHandler):
    

    def get(self, *args,  **kargs):
        
        if self.request.route_kwargs.get('page') == 'robots.txt':
            self.abort(404)
        elif self.request.route_kwargs.get('page') == 'about':
                self.render_template('about.html', {'active':'about'})
        elif self.request.route_kwargs.get('page') == 'terms':
            self.render_template('terms_conditions.html', {'active':'terms'})
        elif self.request.route_kwargs.get('page') == 'contact':
            self.render_template('contact.html', {'active':'contact'})
        else:
            tab = self.request.route_kwargs.get('page')
            if self.user:
                context = self.get_home_context(tab)
                
                context['events'] = context['events'][:15]
                self.render_template('home.html', context = context)
            else:
                context = self.get_index_context(tab)
                
                context['events'] = context['events'][:15]
                self.render_template('index.html', context=context)
    
    def get_home_context(self, tab=None):
        context = {}
        context['active_submenu'] = tab if tab else 'all'
        context['events'] = EventManager.get_events_not_attending(self.user_info['user_id'], category=tab)
        context['left_sidebar'] = 'home'
        return context
    
    def get_index_context(self, tab=None):
        context = {}
        context['active_submenu'] = tab if tab else 'all'
        context['events'] = EventManager.get_event_list(category = tab)
        
        return context
    
    
    
class RpcMainGetEvents(MainHandler, RpcBaseHandler):
    def get(self, *args, **kargs):
        filter_key = self.request.get('filter_key')
        sort_order = self.request.get('sort_order')
        tab = self.request.route_kwargs.get('page')
        if self.user:
            events = EventManager.get_events_not_attending(
                                                                user_id=self.user_info['user_id'], 
                                                                category = tab, filtered_by = filter_key, 
                                                                ordered_by = sort_order)
            
        else:
            events = EventManager.get_event_list(category = tab, filtered_by = filter_key, 
                                                 ordered_by = sort_order)            
        self.prepare_and_serve_events(events)
        
        
       
    def prepare_and_serve_events(self, events):
        
        cursor = self.request.get('cursor')
        if cursor:
            cursor = int(cursor)
            new_cursor = cursor + 15
            if len(events[cursor:]) > 15:
                more = True
            else:
                more = False
            events = events[cursor:new_cursor]
        else:
            if len(events) > 15:
                more = True
            else:
                more = False
            events = events[:15]
            new_cursor = 15
           
        response = {'events':events, 'cursor':new_cursor, 'more':more}
        
        self.send_success_response(response)
              
        
    
              

     
    