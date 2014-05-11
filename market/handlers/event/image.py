#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 8 juil. 2013

@author: Aristote Diasonama
'''
import webapp2
from google.appengine.ext import ndb

from shop.handlers.event.image import ImageHandler


class ImageHandler(ImageHandler):
    
    @webapp2.cached_property
    def event(self):
        event_key = self.request.route_kwargs.get('event_key')
        if not event_key:
            event_key = self.request.get('event_key')
        if not event_key:
            return None
        event = ndb.Key(urlsafe=event_key).get()
        
        return event if event else None