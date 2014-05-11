'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import logging
from django.utils import simplejson


from shop.handlers.ticket.base_handler import BaseHandler

from shop.handlers.base_handler import asso_required

from shop.models.activity import Activity

from shop.shop_exceptions import EventNotFoundException, TicketNotFoundException
from shop.shop_exceptions import TicketEditionFailedError


class EditTicketHandler(BaseHandler):
        
    @asso_required
    def get(self, *args, **kargs):
        try:
            self.render_edit_ticket_form()
        except EventNotFoundException as e:
            #logging.info(e.message)
            self.redirect(self.uri_for('showEvent'))
        except TicketNotFoundException as e:
            #logging.info(e.message)
            self.redirect(self.uri_for('showEvent', event_id=self.event_key.id()))
            
    
    def render_edit_ticket_form(self):
        if not self.event:
            raise EventNotFoundException("No Event id was provided or the event id provided couldn't be found")
        
        if not self.ticket:
            raise TicketNotFoundException("No Ticket id was provided or the ticket id couldn't be found")
            
        context = self.getTemplateContext()
            
        self.render_template('create_ticket.html', context)
        
    def getTemplateContext(self):
        
        context = dict()
        context['ticket'] = self.ticket
        context['edit'] = True
        context['reservation'] = False if self.event.type == 'paid' else True
        context['url_for_editTicket'] = self.uri_for('editTicket', event_id=self.event.key.id(), ticket_id=self.ticket.key.id())
        context['sidebar_active'] = "edit_ticket"
        return context        
               
    
    @asso_required
    def post(self, *args, **kargs):
        
        try:   
            self.edit_ticket_and_return_key()   
            self.redirect(self.uri_for('showEvent', event_id=self.event_key.id()))
        
        except TicketNotFoundException, TicketEditionFailedError:
            raise 
    
    def edit_ticket_and_return_key(self):
        if not self.event or not self.ticket:
            raise TicketNotFoundException("No Ticket to edit provided")
        newData = self.getRequiredPostedData()
        ticket_key = self.ticket.edit(newData)
        
        if ticket_key:
            self.log_this_activity(ticket_key)
        else:
            raise TicketEditionFailedError("The edition of the ticket failed")
        return ticket_key    
    def log_this_activity(self, target):
        self.user.log_activity(Activity(category=4, target = target))



class RpcEditTicketHandler(EditTicketHandler):
    @asso_required
    def post(self, *args, **kargs):
        try:
            ticket_key = self.edit_ticket_and_return_key()
            self.send_success_response(ticket_key)
        
        except TicketNotFoundException as e:
            self.send_failed_response(e.message)
    def send_success_response(self, ticket_key):
        ticket = ticket_key.get()
        ticket_info = ticket.get_ticket_info()
        self.response.out.write(simplejson.dumps(ticket_info))
    
    def send_failed_response(self, message):
        pass

class RpcDeleteTicketHandler(BaseHandler):
    @asso_required
    def post(self, *args, **kargs):
        try:
            self.delete_ticket()
            self.log_this_activity()
            self.send_success_response()
        except TicketNotFoundException as e:
            self.send_failed_response(e)
    
    def delete_ticket(self):
        if not self.ticket:
            raise TicketNotFoundException
        self.ticket.delete_ticket()
    
    def log_this_activity(self):
        self.user.log_activity(Activity(category=8, target = self.event_key))  
    def send_success_response(self):
        self.response.out.write(simplejson.dumps({'message':'success'}))
    def send_failed_response(self, e):
        self.response.out.write(simplejson.dumps({'message':e.message}))
        self.response.set_status(e.code)
