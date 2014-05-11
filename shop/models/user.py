#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import time
import logging
from operator import attrgetter

import sys
from google.appengine.ext import ndb
sys.modules['ndb'] = ndb

import webapp2_extras.appengine.auth.models as model
from webapp2_extras import security

from google.appengine.ext import db
from google.appengine.api import images
import helper_functions as helpers

from .activity import Activity
from .event import Event
from .attendance import Attendance
from .subscription import Subscription


from shop.shop_exceptions import UserAlreadyExistError, NoActivitiesFoundError
from shop.shop_exceptions import LogActivityError

class EmailNotificationsSettings(ndb.Expando):
    """
    Class modeling the authorization of email notifications by the user
    the member of the class:
      - daily_alert :  Daily alert about event user is attending
      - weekly_digest : Weekly alert about event taking place during the week
      - newsletter : EventBuck newsletter
      - help_me : Tricks about using EventBuck
    """
    email_to_use = ndb.StringProperty()
    daily_alert = ndb.BooleanProperty(default = True)
    weekly_digest = ndb.BooleanProperty(default = True)
    newsletter = ndb.BooleanProperty (default = True)
    help_me = ndb.BooleanProperty(default = True)
    
    @classmethod
    def get_settings_for(cls, user_id = None, user_key = None):
        """
        Function to get notifications authorizations for a given user_id or user_key
        If not user_id or not user_key is passed return no authorization.
        """
        if not user_id and not user_key :
            
            return
        if user_key :
            if not isinstance(user_key, ndb.Key):
                user_key = ndb.Key(urlsafe = user_key)
        else:
            user_key = ndb.Key(User, int(user_id))
            
        if user_key:
            notifications_settings = cls.query(ancestor=user_key).get()
            if notifications_settings:
                return notifications_settings
            else:
                
                notifications_settings = EmailNotificationsSettings(parent = user_key, email_to_use = user_key.get().email)
                notifications_settings.put()
                return notifications_settings
    
    def edit(self, new_data):
        """ edit notifications settings 
           Arguments:
              _ new_data : New notifications settings
        """
            
        for key, value in new_data.iteritems():
            setattr(self, key, value)
        return self.put()
        
class UserListOfActivities(ndb.Model):
    """
    A class used to store list of user's activities
    """
    activities = ndb.LocalStructuredProperty(Activity, repeated=True)

class UserIC(ndb.Expando):
    """
    A ndb child of a User object. Encapsulates the user IC
    Attributes:
        - ICu1: represent the IC related to followers 
        - ICu2: represent the IC related to following (only student)
        - ICe1: represent the IC related to events posted
        - Ice2: represent the IC related to events attended (only student)
        
    """
    ICu1 = ndb.FloatProperty(default = 0)
    ICu2 = ndb.FloatProperty(default = 0)
    ICe1 = ndb.FloatProperty(default = 0)
    ICe3 = ndb.FloatProperty(default = 0)
    lastWeekIC = ndb.FloatProperty()
    lastMonthIc = ndb.FloatProperty()
    lastYearIC = ndb.FloatProperty()
    

class User(model.User):
    """
    Class modeling a user. Because it is an expando, we only represent
    required properties, other properties are saved on the fly
   
    Contain personnal information about the seller
    Extend the webapp2 auth User model    
    Properties:
               - event_list: list of event sold by the shop
               - description: description of the seller
               - email: email address of the seller
               - phone: phone number of the seller
               - adresse: address of the seller
               - url : Link to the website of the seller
               - facebook : Link to the facebook of the seller
               _ twitter : Link to the twitter of the seller
               - major : User Major(in case student)
               - events_published: Number of event published
               - picture : User picture
               - list_of_activities : A key to the object containing the list of activities by the user
               
               
    """
    university_name = ndb.StringProperty(default = 'UL')
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    verified = ndb.BooleanProperty(default=False)
    type = ndb.StringProperty()
    list_of_activities = ndb.KeyProperty()
    picture = ndb.BlobProperty()
    
    
    
    def get_key(self):
        return ndb.Key(self.key.kind(), self.key.id())
    
    def get_full_name(self):
        if self.type == 'student':
            return " ".join((self.firstname, self.name))
        return self.name
    def get_name(self):
        if self.type == 'student':
            return self.firstname
        return self.name
    
    def get_user_in_dict(self):
        """
        This function returns the event entity as a dict
        """
        
        user={'type':self.type, 'name':self.name, 'verified':self.verified
                              }
        try:
            user['events_published'] = self.events_published if self.events_published else 0

        except AttributeError:
            user['events_published'] = 0
        try:
            user['description'] = self.description
        except AttributeError:
            user['description'] = None
        
        try:
            user['picture'] = True if self.picture else False
        except AttributeError:
            user['picture'] = False
        
        if self.type == 'student':
            user['firstname'] = self.firstname
            try:
                user ['gender'] = self.gender
            except AttributeError:
                self.gender = 'male'
                self.put_async()
                user['gender'] = 'male'
            try:
                user['major'] = helpers.get_full_major_name(self.major)
            except AttributeError:
                user['major'] = None
            
        user['id'] = self.key.id()
        user['fullname'] = self.get_full_name()
        return user
    
    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
            The raw password which will be hashed and stored
        """
        self.password = security.generate_password_hash(raw_password, length=12)
       
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """
        Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
           A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        logging.info('valid tokens "%s" user "%s"', valid_token, user)
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None
    @classmethod
    def get_by_fb_id(cls, fb_id):
        return User.query(ndb.GenericProperty('fb_id') == fb_id).get()
    
     
    @classmethod
    def create_student(cls, **kwargs):
        """
        Create a user who is a student
        """ 
        kwargs['type'] = 'student'
        kwargs['unique_properties']=['u_email']
        
        return cls._create_a_new_unique_user(**kwargs)
    
    @classmethod
    def create_association(cls, **kwargs):
        """
        Create a user who is an association in a university
        """
        kwargs['type'] = 'asso'
        return cls._create_a_new_unique_user(**kwargs)
     
    @classmethod
    def _create_a_new_unique_user(cls, **kwargs):
        # by default we create a user associated with university laval
        
        kwargs['university_name'] = 'ULaval'

        user_data = cls.create_user(kwargs['email'],
                                    verified=False, **kwargs)   
        
        if not user_data[0]:
            raise UserAlreadyExistError("Unable to create user for email %s because\
            of duplicate keys %s".format(kwargs['email'], user_data[1]))
        return user_data[1]
    
    
    def edit(self, new_data):
        """Function to edit user's data, take a dict of new data
        """
        picture = new_data.get('picture')
        if picture:
            picture = images.resize(picture, 300)
            new_data['picture'] = db.Blob(picture)
            
        for key, value in new_data.iteritems():
            setattr(self, key, value)
        return self.put()
    
    def edit_notifications_settings(self, posted_data):
        email_to_use = posted_data.get('email_to_use')
        if email_to_use == 'u_email':
            posted_data['email_to_use'] = self.u_email
        else:
            posted_data['email_to_use'] = self.email
            
        notifications = self.get_notifications_settings()
        return notifications.edit(posted_data)
        
    
    def verify(self):
        if not self.verified:
            self.verified = True
            self.put()  
    
    
    def create_event_from(self, event_type = 'free',  **kwargs):
        """ Function to create an event and add it to the shop.
            Function takes a dict that contains all arguments we have to assign to an event.
        """
        
        return Event.create_event_from(parent=self.get_key(), event_type=event_type, **kwargs)
        

        
    
    def create_free_event(self, **kwargs):
        return self.create_event_from(**kwargs)
    
    def create_paid_event(self, **kwargs):
        return self.create_event_from(event_type = 'paid', **kwargs)
    
    def get_all_events(self):
        """
        A function to retrieve all events created for this shop
        """
        return  map(Event.get_event_in_dict_extended, self.get_all_free_events())
    
    def get_all_free_events(self):
        """
        A function to retrieve all paid events
        """ 
        return Event.query(ancestor=self.get_key()).filter(Event.deleted == False, Event.type =='free').order(-Event.date_created).fetch(1000)       
    
    def get_all_paid_events(self):
        """
        A function to retrieve all paid events
        """
        return Event.query(ancestor=self.get_key()).filter(Event.deleted==False and Event.type=='paid')
    
    
    @ndb.transactional
    def publish_event(self, event):
        event_key = event.publish_event()
        try:
            self.events_published += 1
        except AttributeError:
            self.events_published = 1
        if self.type == 'student':
            attending_key = self.will_attend_event(event_key)
            self.put()
            return attending_key
        else:
            self.put()
        
            
        
        
    def is_attending_event(self, event_key):
        """
        Check if user is going to attend a given event
        """
        return True if Attendance.query(ancestor=event_key).filter(Attendance.attendee == self.get_key()).get(keys_only = True) else None
    


    
    def subscribe_to_user(self, user_key = None, user_id = None, approved=True):
        """
        A function to enable a user to subscribe to another user
        All subscription is by default approved by the user to subscribe to
        """
        if not(user_key or user_id):
            return
            
        if user_key and not isinstance(user_key, ndb.Key):
            user_key = ndb.Key(urlsafe = user_key)
        elif user_id:
            user_key = ndb.Key(User, user_id)
        subscription = Subscription(parent=self.get_key(), following = user_key, approved = True)
        return subscription.put()
    
    def is_subscribed_to(self, user_key):
        """
        Check if user is going to attend a given event
        """
        return True if Subscription.query(ancestor=self.get_key()).filter(Subscription.following == user_key).get(keys_only = True) else None
    
    def get_subscription_key(self, user_key):
        """Return subscription key of the user
           
           Args:
                user_key: the key of the user the current user is subscribed to
        """
        return Subscription.query(ancestor=self.get_key()).filter(Subscription.following == user_key).get(keys_only = True)
    
    def get_following_keys(self):
        """
        Return two list, first contains the keys of the users followed, and second is the subscription keys
        """
        subscriptions = Subscription.query(ancestor=self.get_key()).fetch(projection=[Subscription.following])
        return map(attrgetter('following'), subscriptions), map(attrgetter('key'), subscriptions)
    
    def get_followers_keys(self):
        """
        Return list of keys of the followers of the user
        """
        subscriptions = Subscription.query(Subscription.following == self.get_key()).fetch(keys_only=True)
        return [subscription_key.parent() for subscription_key in subscriptions]
    
    def log_activity(self, activity):
        """
        This function is used to log each user activity
        
        :param activity:
              an instance of class Activity represents the activity to log
        :return:
            True if the activiy as been logged, and None if failed to log
        """
        
        if not isinstance(activity, Activity) or  activity is None:
            raise LogActivityError("No Activity being logged or Object Provided\
            Not of type Activity")
        list_of_activities_key = self.list_of_activities
        if not isinstance(list_of_activities_key, ndb.Key) or list_of_activities_key is None:
            list_of_activities_key = UserListOfActivities(parent=self.get_key()).put()
            self.list_of_activities = list_of_activities_key
            self.put()
        list_of_activities = list_of_activities_key.get()
        list_of_activities.activities.append(activity)
        list_of_activities.put()
        
       
        
        
    
    def get_first_ten_activities(self):
        return self.get_ten_activities()
    
    def get_ten_activities_starting_from(self, start_cursor):
        return self.get_ten_activities(start_cursor=start_cursor)
    
    def get_ten_activities(self, start_cursor=None):
        """
        This function allows us to get ten activities from the cursor
        if the cursor is not set, we start from the beginning
        """
        
        activities = self.get_all_activities()
        number_of_activities = len(activities) if not start_cursor else len(activities[start_cursor:])
        more = True if number_of_activities>10 else False
        if start_cursor is None:
            results = activities[:10]
        else:
            results = activities[start_cursor: start_cursor+10] if \
            number_of_activities >= start_cursor+10 else activities[start_cursor: ]
        if more:
            next_cursor = start_cursor+10 if start_cursor else 10
        else:
            next_cursor = None
        

        
        if not activities:
            raise NoActivitiesFoundError("There were no activities found")
        
        return (results, next_cursor, more)


    def get_all_activities(self):
        """
        A function to retrieve all user activities in reverse ordered of the
        date they have been added
        """
        list_of_activities_key = self.list_of_activities
        if not list_of_activities_key:
            return []
        
        activities = self.list_of_activities.get().activities
        return list(reversed(activities))
    
    def get_notifications_settings(self):
       
        return EmailNotificationsSettings.get_settings_for(user_key=self.key)
    
            
        