#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''
from shop.handlers.event.base import BaseHandler

from shop.handlers.base_handler import asso_required

from shop.models.event import Event

from shop.shop_exceptions import EventNotFoundException


class ShowEventHandler(BaseHandler):
    
    @asso_required
    def get(self):
        
        try:
            self.try_to_show_the_event()
       
        except EventNotFoundException:
            self.show_all_events()
      
            
    def try_to_show_the_event(self):
        if not self.event:
            raise EventNotFoundException
        
        context = self.get_template_context_showing_one_event()
        self.render_template('view_event.html', context=context)
    
   
    def show_all_events(self):
        context = self.get_template_context_showing_all_events()
        self.render_template('view_event.html', context=context)
    
    
    def get_template_context_showing_one_event(self):
        
        context = dict()
        context['event'] = self.event.get_event_in_dict_extended()
        context['event']['image'] = self.uri_for('imageEvent', event_id = self.event_key.id())
        context['isShowingAllEvents'] = False
        context['sidebar_active'] = "overview"
            
        context['url_for_editEvent'] = self.uri_for('editEvent', event_id = self.event_key.id())
        context['url_to_publish_event'] = self.uri_for('rpc_publishEvent', event_id = self.event_key.id())
        context['url_to_delete_event'] = self.uri_for('rpc_deleteEvent', event_id = self.event_key.id())
        
        if self.event.type == 'paid':
            context.update(self.get_template_context_paid_event())
        
        
        
        return context
    
    def get_template_context_paid_event(self):
        context = dict()
        
        tickets = self.event.get_all_tickets()
        if tickets is not None:
            tickets_urls = map(lambda ticket: self.uri_for('editTicket', 
                              event_id=self.event_key.id(), ticket_id=ticket.key.id()), 
                              tickets.fetch())
        
        context['tickets'] = zip(tickets, tickets_urls) if tickets else None
        context['url_for_createTicket'] = self.uri_for('createTicket', event_id = self.event_key.id())
        context['url_for_rpc_create_ticket'] = self.uri_for('rpc_createTicket', event_id=self.event_key.id())
        
        
    def get_template_context_showing_all_events(self):
        
        events = self.user.get_all_events()
        
        context = dict()
        context['events'] = events
        context['showingAllEvents'] = True
        context['sidebar_active'] = "allEvent"     
        
        return context  