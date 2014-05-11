'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from django.utils import simplejson

from shop.handlers.ticket.base_handler import BaseHandler

from shop.handlers.base_handler import asso_required


from shop.models.activity import Activity

from shop.shop_exceptions import EventNotFoundException
from shop.shop_exceptions import TicketCreationFailedError


class CreateTicketHandler(BaseHandler):
    
    @asso_required
    def get(self, *args, **kargs):
        
        try:
            self.render_create_ticket_form()
            
        except EventNotFoundException:
            self.redirect(self.uri_for('showEvent'))
            
            
    @asso_required
    def post(self, *args, **kargs):
        
        try:
            self.create_ticket_and_return_key()
            self.redirect(self.uri_for('showEvent', event_id=self.event_key.id()))
        
        except EventNotFoundException:
            raise
    
    def get_template_context(self):
            context = dict()
            context['url_for_createTicket'] = self.uri_for('createTicket', event_id=self.event_key.id())
            context['sidebar_active'] = "createEvent"
            context['reservation'] = False if self.event.type == 'paid' else True
            return context
    
    def log_this_activity(self, target):
        self.user.log_activity(Activity(category=2, target=target))
    
    def create_ticket_and_return_key(self):
        """
        This function create a ticket for the current event and return it's key.
        If the event is not set an EventNotFoundException is raised
        """
        if not self.event:
                raise EventNotFoundException("couldn't create the ticket because no event was specified")
        
        postedData = self.getRequiredPostedData()
        
        ticket_key = self.event.create_ticket_from(**postedData)
        
        if ticket_key:
            self.log_this_activity(ticket_key)
        else:
            raise TicketCreationFailedError("couldn't create the ticket because of internal problems")
        return ticket_key
    def render_create_ticket_form(self):
        """
        This function render a form for the current event if the event is set.
        If there is no event set, it raises an event not found exception
        """
        
        if not self.event:
            raise EventNotFoundException
            
        context = self.get_template_context()
        self.render_template('create_ticket.html', context)
            
        

class RpcCreateTicketHandler(CreateTicketHandler):
    
    @asso_required
    def post(self, *args, **kargs):
        try:
            ticket_key = self.create_ticket_and_return_key()
            self.send_success_response(ticket_key)
        
        except EventNotFoundException as e:
            self.send_failed_response(e.message)
            
    def send_success_response(self, ticket_key):
        ticket = ticket_key.get()
        ticket_info = ticket.get_ticket_info()
        self.response.out.write(simplejson.dumps(ticket_info))
    
    def send_failed_response(self, message):
        pass
