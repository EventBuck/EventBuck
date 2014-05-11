'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''
import webapp2

from google.appengine.ext import ndb 

import helper_functions as helpers
from shop.handlers.event.base import BaseHandler as EventBaseHandler
from shop.models.ticket import Ticket


class BaseHandler(EventBaseHandler):
              
    """
    This is an abstract class that to create event based class
    """
    
    
    def getRequiredPostedData(self):
        """
        This function helps to clean and prepare all data related to event.
        This is a global check function for posted data
        
        return a dict of all the edited values
        """
        listOfNamesOfDataToClean = ['category', 'sub_category','description', 'row', 'section', 'price', 'quantity', 'sell_start', 'sell_end']
        
        cleanedData = self.cleanPostedData(listOfNamesOfDataToClean)
        
        if cleanedData.get('price'):   
            cleanedData['price'] = float(cleanedData.get('price'))
        if cleanedData.get('quantity'):
            cleanedData['quantity'] = int(cleanedData.get('quantity'))
        if cleanedData.get('sell_start'):
            cleanedData['sell_start'] = helpers.jquery_datepicker_parser(cleanedData['sell_start'])
        if cleanedData.get('sell_end'):
            cleanedData['sell_end'] = helpers.jquery_datepicker_parser(cleanedData['sell_end'])
            
        return cleanedData
            
            
    
    @webapp2.cached_property
    def ticket(self):
        ticket_id = self.request.route_kwargs.get('ticket_id')
        if not ticket_id:
            ticket_id = self.request.get('ticket_id')
        
        return Ticket.get_by_id(int(ticket_id), parent = self.event_key) if ticket_id else None
        
