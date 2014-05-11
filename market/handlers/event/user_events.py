#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 27 juil. 2013

@author: Aristote Diasonama
'''

from shop.handlers.event.show import ShowEventHandler as ShopShowEvent
from shop.handlers.event.create import CreateEventHandler as ShopCreateEvent
from shop.handlers.event.edit import EditEventHandler as ShopEditEvent
from market.handlers.base import BaseHandler 
from market.lib.event import EventManager


from shop.handlers.base_handler import user_required

class CreateEventHandler(BaseHandler, ShopCreateEvent):
    @user_required
    def get(self):
       
        self.render_template('create_event.html', {'sidebar_active':"createEvent", 'active':'createEvent'})
    @user_required
    def post(self):
        ShopCreateEvent.post(self)
        self.redirect(self.uri_for('marketUserEvents', event_id = self.event_key.id()))    

class EditEventHandler(BaseHandler, ShopEditEvent):
    @user_required
    def get(self, *args, **kargs):
        if not self.event:
            self.redirect(self.uri_for('createEvent'))
            
        context = self.get_template_context()
      
        self.render_template('create_event.html', context=context)
    def get_template_context(self):
        context = super(EditEventHandler, self).get_template_context()
        context['event']['image'] = EventManager._get_event_image(context['event'])
        context['url_for_editEvent'] = self.uri_for('rpcEditEvent', event_id = self.event.key.id())
        return context
    
    @user_required
    def post(self, *args, **kargs):
        ShopEditEvent.post(self, *args, **kargs)
        self.redirect(self.uri_for('marketUserEvents', event_id=self.event.key.id()))
        
class ShowEventHandler(BaseHandler, ShopShowEvent):
    @user_required
    def get(self):  
        context = self.get_template_context()
        self.render_template('my_events.html', context)
    def get_template_context(self):
        if self.event:
            context = self.get_template_context_showing_one_event()
            context['event']['image'] = EventManager._get_event_image(context['event'])
            context['event']['stat'] = EventManager.get_event_stats(self.event.key.urlsafe())
        else:
            context = self.get_template_context_showing_all_events()
        
        context['left_sidebar'] = 'my_events'
        return context
    def get_template_context_showing_one_event(self):
        context = super(ShowEventHandler, self).get_template_context_showing_one_event()
        context['url_for_editEvent'] = self.uri_for('marketEditEvent', event_id = self.event.key.id())
        return context
    
    def get_template_context_showing_all_events(self):
        events = EventManager.get_event_list() + EventManager.get_event_list(recent = True)
        context = dict()
        context['events'] = events
        context['showingAllEvents'] = True
        context['sidebar_active'] = "allEvent"
        
        return context
