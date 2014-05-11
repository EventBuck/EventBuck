#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 1 juil. 2013

@author: macbookuser
'''
import random
import datetime
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from concurrent.futures.thread import ThreadPoolExecutor
from shop.handlers.base_handler import BaseHandler, user_required
from shop.handlers.event.create import CreateEventHandler
from market.models.mall import Mall
from shop.models.user import User
from shop.models.subscription import Subscription
from market.lib.event import EventManager
import memcache
import webapp2


def init_number_users():
    number_of_users = User.query(User.type == 'student').count()
    memcache.init_total_users(number_of_users)


def init_number_subscriptions():
    clean_up_subscription()
    users = User.query().fetch()
    for user in users:
        followers = Subscription.query(Subscription.following == user.key).count()
        following = Subscription.query(ancestor = user.key).count()
        memcache.init_followers_number(user.key.id(), followers)
        memcache.init_following_number(user.key.id(), following)

def clean_up_subscription():
    subscriptions = Subscription.query().fetch()
    for subscription in subscriptions:
        if not subscription.key.parent.get():
            subscription.key.delete()
            continue
        if not subscription.following.get():
            subscription.key.delete()

def dev_server_only(function):
    """
    This a decorator to apply to functions restricted to event of type paid
    If the function is applied to another type, it raises an InvalidEventError
    """
    def check_server(self, *args, **kwargs):
        from main import debug
        
        if not debug:
            webapp2.abort(403)
        return function(self, *args, **kwargs)
    
    return check_server

class SetUpGamification(BaseHandler):
    def get(self):
        task = taskqueue.add(url='admin/tasks/setup/gamification')
    def post(self):
        try:
            with ThreadPoolExecutor(max_workers = 2) as e:
                e.submit(init_number_users)
                e.submit(init_number_subscriptions)
            self.init_number_users()
            
        except:
            raise
    
    
    
    
    
    
    
class UpdateEvent(BaseHandler):
    def get(self):
        tracker_list = self.user.get_all_events()
        for activity in tracker_list:
            activity.type = 'paid'
            activity.put()
        self.redirect(self.uri_for('shopMain'))
        
class PopulateEvent(CreateEventHandler):
    
    @dev_server_only
    @user_required
    def get(self):
        categories = ["party", "other", "sport","academic"]
        for i in range(1,50):
            event_data = {
            'name' : "FreeEvent "+str(i),
            'date_event' : datetime.datetime.now() + datetime.timedelta(hours = i*random.randrange(2, 50)),
            'venue_name' : "Venue " + str(i),
            'venue_addresse' : "Addresse " + str(i),
            'category' : categories[random.choice([0,1,2,3])],
            'terms' : "Terms for event number " + str(i),
            'description' : "This is description for event number " + str(i) }
            
            event = self.user.create_free_event(**event_data)
            EventManager.publish_event(event.id(), self.user)
        self.response.out.write('{} created successfully'.format(i))



class CreateShop(BaseHandler):
    @dev_server_only
    def get(self):
        mall = Mall.query().get()
        if not mall:
            mall = Mall()
        mall.create_event_list()
        self.response.out.write(mall.upcoming_event_list)

class VerifyUser(BaseHandler):
    @dev_server_only
    def get(self):
        self.user.verified = True
        self.user.put()
        self.response.out.write("User is verified: {}".format(self.user.verified))

class AppendAuthId(BaseHandler):
    
    def get(self):
        mall = Mall()
        student_list = filter(lambda user: user.type == 'student', mall.get_all_users()[0])
        
        for user in student_list:
            user.auth_ids.append(user.u_email)
            
        ndb.put_multi(student_list)
        self.response.out.write('{} update sucessfully'.format(len(student_list)))
