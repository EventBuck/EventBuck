#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 28 août 2013

@author: Aristote Diasonama
'''
from google.appengine.ext import ndb

class ContactMessage(ndb.Model):
    """An absolute class to represent a message sent by a user through the website
    """
    subject = ndb.StringProperty(required=True)
    message = ndb.TextProperty(required = True)
    date_sent = ndb.DateTimeProperty(auto_now_add=True)
    read = ndb.BooleanProperty(default=False)
    
    @classmethod
    def create_message(cls, user_key=None, **kwargs):
        """
        Create a message and save it to the database
        """
        if user_key is None:
            message = VisitorMessage(subject=kwargs.get('subject'),
                                     message=kwargs.get('message'),
                                     visitor_type = kwargs.get('type'),
                                     visitor_name = kwargs.get('name'),
                                     visitor_email = kwargs.get('email'),
                                     )
        else:
            message = UserMessage(subject=kwargs.get('subject'),
                                  message=kwargs.get('message'),
                                  user_key = user_key)
        
        return message.put() 

class UserMessage(ContactMessage):
    """A class to represent a message sent by a user already registered
    """
    user_key = ndb.KeyProperty(required=True)

class VisitorMessage(ContactMessage):
    """A class to represent a message sent by a prospected user
    """
    visitor_type = ndb.StringProperty()
    visitor_name = ndb.StringProperty()
    visitor_email = ndb.StringProperty(required=True)
    
    
    