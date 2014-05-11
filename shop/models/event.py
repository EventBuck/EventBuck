#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import datetime
import time
from google.appengine.ext import ndb
from google.appengine.api import images

from .ticket import Ticket
from shop.shop_exceptions import InvalidEventError
from shop.shop_exceptions import EventInMarketError





def only_paid_event(function):
    """
    This a decorator to apply to functions restricted to event of type paid
    If the function is applied to another type, it raises an InvalidEventError
    """
    def check_paid_event(self, *args, **kwargs):
            
        if not self.type == 'paid':
            raise InvalidEventError("The function {} is reserved to event of type paid".format(function))
        return function(self, *args, **kwargs)
    
    return check_paid_event

class Review(ndb.Model):
    """
    Review class models a review given to an event by a user
    Attributes are:
        - reviewer:
        - score: 
        - date_reviewed:
    """
    reviewer_id = ndb.StringProperty(required=True) 
    date_reviewed = ndb.DateTimeProperty(auto_now=True)
    score = ndb.IntegerProperty(choices=[1,2,3,4,5])
    
    @classmethod
    def get_reviews_for(cls, event_key):
        #for now limit to 1000
        return Review.query(ancestor=ndb.Key(urlsafe=event_key)).fetch(1000)
    @classmethod
    def get_review_by(cls, user_id, event_key):
        return cls.query(ancestor=ndb.Key(urlsafe=event_key)).filter(cls.reviewer_id==str(user_id)).get()
    
class EventProperty(ndb.Expando):
    """
    This a class where to record additional property of an event.
    It is used to add property on fly without modifying the Event class structure.
    It should always be a datastore child of an event.
    Properties that may be found are:
       image_url : if the event is a facebook event
    """
    is_facebook = ndb.BooleanProperty(default = False)
    
class EventStat(ndb.Expando):
    """
    This class is used to encapsulate the stat of a given event
    """
    unique_views = ndb.IntegerProperty(default = 0)
    total_views = ndb.IntegerProperty(default = 0)
    rating = ndb.FloatProperty(default = 0)
    rating_numbers = ndb.IntegerProperty(default = 0)
    girl_numbers = ndb.IntegerProperty(default = 0)
    boy_numbers = ndb.IntegerProperty(default = 0)
    IC = ndb.FloatProperty(default = 0)
    reviews = ndb.JsonProperty(default = {})
    visits = ndb.JsonProperty(default = {})
    
    
class Event(ndb.Model):
    """
    Class modeling an event being organized
    An object of this class must be a child of a parent which is an object of class Shop
    """
    type = ndb.StringProperty(default = 'free')
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required = True)
    category = ndb.StringProperty(default = 'other', choices=['party','sport','academic','other'])
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_modified = ndb.DateTimeProperty(auto_now=True)
    date_event = ndb.DateTimeProperty(required=True)
    geo_location = ndb.GeoPtProperty()
    venue_name = ndb.StringProperty(required=True)
    venue_addresse = ndb.StringProperty(required=True)
    published = ndb.BooleanProperty(default=False)
    date_published = ndb.DateTimeProperty()
    venue_picture = ndb.BlobProperty()
    venue_picture_key = ndb.BlobKeyProperty()
    deleted = ndb.BooleanProperty(default = False)
    cancelled = ndb.BooleanProperty(default = False)
    terms = ndb.TextProperty()
    url = ndb.StringProperty()
    
    @classmethod
    def _post_delete_hook(cls, key, future):
        property_key = EventProperty.query(ancestor = key).get(keys_only=True)
        if property_key:
            property_key.delete()
     
        
    
    
    @classmethod
    def create_event_from(cls, parent, event_type = 'free',  **kwargs):
        """ Function to create an event and add it to the shop.
            Function takes a dict that contains all arguments we have to assign to an event.
        """
        
        
         
        event = cls(parent=parent, name=unicode(kwargs['name']), date_event=kwargs['date_event'],
                      venue_name=kwargs['venue_name'], venue_addresse=kwargs['venue_addresse'], type = event_type)
        

            
        event.populate(description=kwargs.get('description'),
                       geo_location=kwargs.get('geo_location'), terms = kwargs.get('terms'), url=kwargs.get('url'),
                       category = kwargs.get('category', 'other'), published = kwargs.get('published', False))
        
        event_key = event.put()
        
        if event_key:
            is_facebook = kwargs.get('is_facebook')
            if is_facebook:
                event_property = EventProperty(parent = event_key, is_facebook = True, image_url = kwargs.get('image_url'))
                event_property.put()        
        
        return event_key
    
    
    def get_key(self):
        return self.key
      
    def get_event_in_dict(self):
        """
        This function returns the event entity as a dict
        """
        event = dict()
        
        
        properties_to_return=['type', 'name', 'date_published', 'date_event', 'description',
                              'venue_name', 'venue_addresse', 'category', 'terms','deleted','url']
        
        for prop in properties_to_return:
            event[prop] = self.__getattribute__(prop)
        #keep terms and description formatted
        event['description'] = event['description'].replace('\n', '<br>\n')
        if event['terms']:
            event['terms'] = event['terms'].replace('\n', '<br>\n')

        if event['date_published']:
            event['date_published'] = time.mktime(event['date_published'].timetuple()) 
        event['date_event'] = time.mktime(event['date_event'].timetuple())
        event['parent'] = self.key.parent().urlsafe()
        event['key'] = self.key.urlsafe()
        event['id'] = self.key.id()
        event_property = self.get_property()

        # work around to support event created with venue_picture attribute
        try:
            event['has_image'] = True if self.venue_picture else False
            if self.venue_picture_key: 

                event['image_url'] = images.get_serving_url(self.venue_picture_key) 
            else:
                if event_property and event_property.is_facebook:
                    event['image_url'] = event_property.image_url
                    event['is_image_extern'] = True
        except:
            event['has_image'] = False
            
            if self.venue_picture_key:

                event['image_url'] = images.get_serving_url(self.venue_picture_key) 
            else:
                if event_property and event_property.is_facebook:
                    event['image_url'] = event_property.image_url
                    event['is_image_extern'] = True
                    
                    
        return event
    def get_event_in_dict_extended(self):
        """
        This function is same as get_event_in_dict but with more properties
        """ 
        event = self.get_event_in_dict()
        event['published'] = self.published
        event['date_modified'] = time.mktime(self.date_modified.timetuple())
        event['date_created'] = time.mktime(self.date_created.timetuple())
        return event
    
    def get_property(self):
        return EventProperty.query(ancestor = self.key).get()
    
    def edit(self, **kwargs):
        """
        This is an instance method that help to modify an event, it does a mass modifying checking if the property
        is defined in the dict given. If a given property is specified, it is then modified
        
        Returns nothing
        
        param args:
            a dict that contains the parameters to be modified
        """
        
        for key, value in kwargs.iteritems():
            if isinstance(value, str):
                value = unicode(value)
            setattr(self, key, value)
        venue_picture_key = kwargs.get('image')
        
            
        if venue_picture_key:
            
            
            self.venue_picture_key = venue_picture_key
        
        
        return self.put()
    
       
    
    def publish_event(self):
        """
        A function to publish the event to the markets
        """
        if self.published is True:
            return
        if not self.validate_event():
            raise InvalidEventError("The event being published is invalid")
        
        self.published = True
        self.date_published = datetime.datetime.now()
        
        return self.put()
    

    
    def delete_event(self):
        """
        This function deletes an event.
        2 cases are here:
           1. When the vent is not published the event is deleted from the database
           2. When the event is published, 2 scenarios:
             1. If the event has already taken place, set the deleted flag to True
             2. If the event is still to take place, raise an EventInMarket Exception
        """
        if not self.published :
            self.key.delete()
        if self.published:
            #if self.date_event < datetime.datetime.now():
                self.deleted = True
                self.put()
            #else:
                #raise EventInMarketError
    
    @only_paid_event
    def create_ticket_from(self, **kwargs):
        """
        Function to create a ticket child of this event
        this an ndb transaction
        """
        ticket = Ticket(parent=self.get_key(), price=kwargs['price'], quantity=kwargs['quantity'])
        ticket.category = kwargs.get('category', 'general')
        
        if ticket.category == 'specifique':
            ticket.category = kwargs['sub_category']
        if kwargs.get('row', None):
            ticket.row = kwargs['row']
        
        if kwargs.get('section', None):
            ticket.section = kwargs['section']
        
        if kwargs.get('description', None):
            ticket.description = kwargs['description']
        if kwargs.get('sell_start', None):
            ticket.sell_start = kwargs['sell_start']
        if kwargs.get('sell_end', None):
            ticket.sell_end = kwargs['sell_end']
        
        
        return ticket.put()
    
    @only_paid_event
    def get_ticket_by_id(self, ticket_id):
        """
        Returns the ticket provided its id
        """
        
        return Ticket.get_by_id(ticket_id, parent=self.get_key())
    
    @only_paid_event
    def get_all_tickets(self):
        """
        A function to retrive all tickets created for this shop
        """
        tickets = Ticket.query(ancestor=self.get_key())
        return  tickets if tickets.get() else None   
    
    @only_paid_event
    def delete_ticket(self, ticket_id):
        """
        This function deletes a ticket provided its id if the event is not published.
        If the event is published, it raises a EventInMarketError exception
        """
        if self.published:
            raise EventInMarketError
        
        self.get_ticket_by_id(ticket_id).delete_ticket()
    
    def validate_event(self):
        """
        A function that validate an event before publishing it !
        
        An event is valid if it has tickets and also that its
        event date is not passed
        """
        valid = self.date_event > datetime.datetime.now()
        
        if self.type == 'paid':
            return valid and self.validate_paid_event()
        else:
            return valid
    
    @only_paid_event
    def validate_paid_event(self):
        """
        A function that validate an event before publishing it !
        
        An event is valid if it has tickets and also that its
        event date is not passed
        """
        has_tickets = True if self.get_all_tickets() else False
        
        return has_tickets 

    
    