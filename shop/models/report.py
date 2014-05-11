#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 30 ao�t 2013

@author: Aristote Diasonama
'''
import time
from google.appengine.ext import ndb
from event import Event
from user import User


class Report(ndb.Model):
    """A class that represents a report of an event as a malicious one
    """
    reported_by = ndb.KeyProperty(kind=User, required=True)
    event = ndb.KeyProperty(kind=Event, required=True)
    reported_time = ndb.DateTimeProperty(auto_now_add=True)
    examined = ndb.BooleanProperty(default = False)
    examined_by = ndb.KeyProperty(kind=User)
    examined_time = ndb.DateTimeProperty()
    decision = ndb.TextProperty()
    
    def get_report_in_dict(self):
        """
        This function returns the report entity as a dict
        """
        report = dict()
        properties_to_return=['reported_by', 'event', 'reported_time', 'examined', 'examined_by', 'examined_time', 'decision']
        
        for prop in properties_to_return:
            report[prop] = self.__getattribute__(prop)
        
        report['reported_time'] = time.mktime(report['reported_time'].timetuple())
        if report['examined_time']:
            report['examined_time'] = time.mktime(report['examined_time'].timetuple())
        report['key'] = self.key.urlsafe()
        report['id'] = self.key.id()
        
        return report
    
    @classmethod
    def create_report(cls, user_key, event_key):
        report = Report(reported_by = user_key, event = event_key)
        return report.put()
    @classmethod
    def is_report_exist(cls, event_key):
        return Report.query(Report.event == event_key).get(keys_only = True)
    @classmethod
    def get_all(cls):
        return Report.query().order(Report.reported_time).fetch(1000)
    