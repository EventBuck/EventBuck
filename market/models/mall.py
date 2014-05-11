#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 7 juil. 2013

@author: Aristote
'''
import bisect
import datetime
import time
from itertools import izip
from google.appengine.ext import ndb
from shop.models.event import Event
from shop.models.user import User
from operator import attrgetter
from market.market_exceptions import NoEventsFoundException


REVIEW_TIME = datetime.timedelta(days=30)

class Mall(ndb.Model):
    """This is an entity that serves to store upcoming_events and all users
        Attributes:
            - current_event_list: Events that have yet to take place or taken place
                                  within the past 30 days
            
    """
    
    current_event_list = ndb.JsonProperty(repeated=True)
    user_list = ndb.JsonProperty(repeated=True)
    last_updated_user = ndb.DateTimeProperty()
    last_edited_event = ndb.DateTimeProperty() 
    last_archived = ndb.DateTimeProperty()
    @classmethod
    def get_or_create(cls):
        """
        This function is used to get the instance of the class Mall
        if the instance doesn't exist, create one
        """
        mall = cls.query().get()
       
        if mall:
            return mall 
        else:
            mall = cls()
            if not mall.update_mall():
                mall.put();
                return mall
            return mall
    def update_mall(self):
        
        return self.update_event_list() or self.update_user_list()
    def update_event_list(self):
        
        if not self.current_event_list:
            self.create_event_list()
        else:
            
            updated =  self.add_new_events() or self.delete_passed_event()
            if updated:
                self.put()
            
            return updated
            
    
    
    def create_event_list(self):
        last_edited, event_list = self.get_all_published_event()
        if not event_list:
            return
        event_list = self.get_formatted_events_from(event_list)
        self.current_event_list = event_list
        self.last_edited_event = last_edited
        self.put()
    
    def get_all_published_event(self):
        
        event_list = Event.query().filter(Event.published == True,Event.deleted==False,
                                          Event.type == 'free', Event.date_event > (datetime.datetime.now())-REVIEW_TIME)
        if not event_list.get():
            return None, None
        else:
            event_list = event_list.order(Event.date_event)
            #on supposera qu'il n'y aura pas plus de 2000 events en l'espace d'un mois
            event_list = event_list.fetch(2000)
            last_edited = sorted(event_list, key=attrgetter('date_modified'),reverse=True)[0].date_modified
            
            return last_edited, event_list
        
    def delete_passed_event(self):
        ordered_date_events = map(lambda event: event['date_event'], self.current_event_list)
        index = bisect.bisect(ordered_date_events, time.mktime((datetime.datetime.now()-REVIEW_TIME).timetuple()))
        if index == 0:
            return False
        #TODO: implement a way to calculate the final IC of the event.
        self.current_event_list = self.current_event_list[index: ]
        return True
    
    def add_new_events(self):
        last_edited, event_list = self.get_updated_event_list(self.last_edited_event)
            
        if not event_list:
            return False
        else:
            self.last_edited_event = last_edited
                 
            event_list = self.get_formatted_events_from(event_list)
        
            self.current_event_list.extend(event_list)
            
            #remove duplicate event with same key keeping the latest added
            self.current_event_list = dict(izip(map(lambda event: event['key'], self.current_event_list), self.current_event_list)).values()
            
            #remove deleted event
            self.current_event_list = filter(lambda event: not event.get('deleted'), self.current_event_list)
            
            self.current_event_list.sort(key=lambda event:event['date_event'])
                
            return True
                        
            
    
    def get_updated_event_list(self, edited_after):
        """
        This is a function to get the list of available events
        """
        
        
        event_list = Event.query().filter(Event.published == True,
                                          Event.type == 'free', Event.date_modified > edited_after)
        
        if not event_list.get():
            return None, None
        
        event_list = event_list.order(-Event.date_modified)
        last_update_time = event_list.get().date_modified
        
        event_list = event_list.fetch(2000)
        
        event_list = filter(lambda event: event.date_event > (datetime.datetime.now()-REVIEW_TIME), event_list)
        
        if len(event_list) == 0:
                return None, None
            
        return last_update_time, event_list
         
         
    def get_formatted_events_from(self, event_list):
        
        if not event_list: 
            return None
        return map(Event.get_event_in_dict, event_list)
    
    
    
    def get_current_events(self):
        if self.current_event_list:
            return self.current_event_list 
        else:
            self.update_event_list()
            if self.current_event_list:
                return self.current_event_list
            else:
                raise NoEventsFoundException

    def update_user_list(self):
        if not self.user_list:
            self.create_user_list()
        else:
            
            updated = self.add_new_users()
            if updated:
                self.put()
            
            return updated
    
    def create_user_list(self):
        last_updated, user_list = self.get_all_users()
        if not user_list:
            return
        user_list = self.get_formatted_users_from(user_list)
        self.user_list = user_list
        self.user_list.sort(key=lambda user: user['fullname'])
        self.last_updated_user = last_updated
        self.put()
    
    def get_all_users(self):
        
        user_list = User.query()
        if not user_list.get():
            return None, None
        else:
            
            user_list = user_list.fetch(1000)
            
            
            last_edited = sorted(user_list, key=attrgetter('updated'),reverse=True)[0].updated
            
            return last_edited, user_list
    
    def add_new_users(self):
        last_updated, user_list = self.get_updated_user_list(self.last_updated_user)
            
        if not user_list:
            return False
        else:
            self.last_updated_user = last_updated
                 
            user_list = self.get_formatted_users_from(user_list)
        
            self.user_list.extend(user_list)
            
            #remove duplicate users with same key keeping the latest added
            self.user_list = dict(izip(map(lambda user: user['id'], self.user_list), self.user_list)).values()
            
            #remove deleted user, TODO
            #self.user_list = filter(lambda user: not user.get('deleted'), self.user_list)
            
            self.user_list.sort(key=lambda user: user['fullname'])
                
            return True    
    
    def get_updated_user_list(self, updated_after):
        """
        This is a function to get the list of available events
        """
        
        
        user_list = User.query().filter(User.updated > updated_after)
        
        if not user_list.get():
            return None, None
        
        user_list = user_list.order(-User.updated)
        last_update_time = user_list.get().updated
        
        user_list = user_list.fetch(1000)
        
        
        if len(user_list) == 0:
                return None, None
            
        return last_update_time, user_list
    
    def get_formatted_users_from(self, user_list):
        
        if not user_list: 
            return None
        return map(User.get_user_in_dict, user_list)

    def get_users_list(self):
        if self.user_list:
            return self.user_list
        else:
            self.update_user_list()
            if self.user_list:
                return self.user_list
            else:
                return None  
        
        