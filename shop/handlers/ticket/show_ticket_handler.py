'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''


from .base_handler import BaseHandler

from shop.handlers.base_handler import asso_required

from shop.models.ticket import Ticket

from shop.shop_exceptions import EventNotFoundException, TicketNotFoundException


class ShowTicketHandler(BaseHandler):
    @asso_required
    def get(self, *args, **kargs):
        
        try:
            self.try_to_show_the_ticket()

        except TicketNotFoundException:
            self.show_all_tickets()            
  
                      
        except EventNotFoundException :
            self.redirect(self.uri_for('showEvent'))
        

    
    def try_to_show_the_ticket(self):
        if not self.event:
            raise EventNotFoundException("No Event id was provided or the event id provided couldn't be found")
        
        if not self.ticket:
            raise TicketNotFoundException
            
        context = self.get_template_context_showing_one_ticket()
            
        self.render_template('view_ticket.html', context)    
    
    def show_all_tickets(self):
        context = self.get_template_contex_showing_all_tickets()
        self.render_template('view_ticket.html', context)        
        
            
    
    def get_template_context_showing_one_ticket(self):
        
        context = dict() 
        context['ticket'] = self.ticket
        context['url_for_editTicket'] = self.uri_for('editTicket', event_id=self.event_key.id(), ticket_id=self.ticket.key.id())
        
        return context
    
    def get_template_contex_showing_all_tickets(self):
        
        tickets = self.event.get_all_tickets()
        tickets.order(Ticket.price)
        
        #We put all tickets in a list which contains tuples formed by a url to view the ticket and the ticket itself
        #in the form of ('shops/showTicket/109594/10934', ticket)
        tickets = zip(map(lambda ticket: self.uri_for('showTicket', event_id=self.event_key.id(), ticket_id=ticket.key.id()), tickets), tickets)            
        
        context = dict()
        context['tickets'] = tickets
        context['all'] = True
        
        return context        
        