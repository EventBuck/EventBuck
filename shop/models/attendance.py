#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 26 juil. 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb
from operator import attrgetter

class Attendance(ndb.Model):
    """
    Class modeling an attendance.
    """
    attendee = ndb.KeyProperty(required=True)
    status = ndb.StringProperty(default='going')
    date_event = ndb.DateTimeProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def get_user_attending(cls, event_key):
        attendances = cls.query(ancestor=event_key).fetch()
        return map(attrgetter('attendee'), attendances)