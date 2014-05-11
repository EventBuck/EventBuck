#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import logging
import webapp2

from google.appengine.ext import ndb

import helper_functions as helpers
from shop.handlers.base_handler import BaseHandler as ShopBaseHandler

from shop.models.event import Event


class BaseHandler(ShopBaseHandler):
    """
    This is an abstract class that to create event based class
    """
    def getRequiredPostedData(self):
        """
        This function helps to clean and prepare all posted data related to event.
        This is a global check function for posted data
        
        return a dict of all the edited values
        """
        
            
        listOfNamesOfDataToClean = ['name', 'description', 'venue_addresse', 'venue_name', 'geo_location', 'date_event', 'terms', 'category', 'url', 'is_facebook', 'image_url']  # list of editable property
            
        
            
        cleanedData = self.cleanPostedData(listOfNamesOfDataToClean)    
      
        if cleanedData.get('geo_location'):
            cleanedData['geo_location'] = helpers.MakeGeoPointFromString(cleanedData['geo_location'])
            logging.info(cleanedData['geo_location'])
        
        if cleanedData.get('date_event'):
            cleanedData['date_event'] = helpers.jquery_datepicker_parser(cleanedData['date_event'])
        
        
        
        return cleanedData
    
    @webapp2.cached_property
    def event(self):
        event_id = self.request.route_kwargs.get('event_id')
        if not event_id:
            event_id = self.request.get('event_id')
        if event_id:
            event = Event.get_by_id(int(event_id), parent=self.key)
            print(self.key, event)
        else:
            event_key = self.request.get('event_key')
            if not event_key:
                event_key = self.request.route_kwargs.get('event_key')
            if event_key:
                event = ndb.Key(urlsafe=event_key).get()
            else:
                return None
        
        return event if event else None
    
    @webapp2.cached_property
    def event_key(self):
        return ndb.Key(self.event.key.kind(), self.event.key.id()) if self.event else None
