'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb

from helper_functions import format_datetime

class Reservation(ndb.Model):
    """
    Class modeling a reservation of a place or something
    """
    quantity = ndb.IntegerProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_modified = ndb.DateTimeProperty(auto_now=True)
    sold = ndb.IntegerProperty(default = 0)
    description = ndb.TextProperty()
    sell_start = ndb.DateTimeProperty(required = True)
    sell_end = ndb.DateTimeProperty( required = True)
       
class Ticket(Reservation):
    """
    Class modeling a ticket to an invent.
    Instance must be child of an Event Object.
    """
    category = ndb.StringProperty(default="general")
    price = ndb.FloatProperty(required=True)
    quantity = ndb.IntegerProperty(required=True)
    section = ndb.StringProperty()
    row = ndb.StringProperty()
    sold = ndb.IntegerProperty(default=0)

    
    def edit(self, args):
        """
        This is an instance method that help to modify a ticket, it does a mass modifying checking if the property
        is defined in the dict given. If a given property is specified, it is then modified
        
        Returns nothing
        
        param args:
            a dict that contains the parameters to be modified
        """        
        for key, value in args.iteritems():
            setattr(self, key, value)
        
        return self.put()
    
    def get_ticket_info(self):
        """
        Function to get information about the ticket
        return a dict that contains info about the ticket
        """
        list_of_info =['category', 'price', 'quantity', 'section', 'row', 'sell_start', 'sell_end']
        
        ticket_info = dict()
        
        for attribute in list_of_info:
            ticket_info[attribute] = getattr(self, attribute)
            
        ticket_info['sell_start'] = format_datetime(ticket_info['sell_start'], format_type="medium")
        ticket_info['sell_end'] = format_datetime(ticket_info['sell_end'], format_type="medium")
        return ticket_info 
    
    def delete_ticket(self):
        """
        This function deletes is used to delete a ticket
        """
        self.key.delete()
