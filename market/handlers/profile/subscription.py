#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 5 ao�t 2013

@author: Aristote Diasonama
'''
import webapp2
from shop.handlers.base_handler import RpcBaseHandler
from market.handlers.main import RpcMainGetEvents
from market.handlers.base import BaseHandler
from shop.handlers.base_handler import user_required
from google.appengine.ext import ndb
from shop.models.activity import Activity


from market.lib.subscription import SubscriptionManager
from market.lib.event import EventManager
from .view import ViewProfileHandler

class RpcSubscribe(RpcBaseHandler):
    @webapp2.cached_property
    def user_key_subscribing_to(self):
        return ndb.Key(self.user_model, int(self.request.route_kwargs.get('user_id')))
    @webapp2.cached_property
    def subscription_key(self):
        
        return ndb.Key(urlsafe = self.request.get('subscription_key')) if self.request.get('subscription_key') else None
    @user_required
    def post(self, *args, **kargs):
        if self.subscription_key:
                SubscriptionManager.delete_subscription(self.subscription_key, 
                                                        self.user_key_subscribing_to.id(), 
                                                        self.user_info['user_id'])
                self.unsubscribe()
                self.log_this_activity() 
                self.send_success_response()
        else:
                      
                if not self.user.is_subscribed_to(self.user_key_subscribing_to):
                    subscription_key = SubscriptionManager.subscribe_user_to(self.user_info['user_id'], self.user_key_subscribing_to.id())
                    if subscription_key:
                        subscription_key = subscription_key.urlsafe()    
                        self.log_this_activity()
                        self.send_success_response(message=subscription_key)
                else:
                    self.send_success_response(message="utilisateur déjà abonné")
        
                        
    def log_this_activity(self):
        if self.subscription_key:
            self.user.log_activity(Activity(category=11, target=self.user_key_subscribing_to))
        else:   
            self.user.log_activity(Activity(category=10, target=self.user_key_subscribing_to))

class ShowConnections(ViewProfileHandler):
    @user_required
    def get(self, *args, **kargs):
        context = self.get_template_context()
        context.update(self._get_profile_info())
        self.render_template('connections.html', context)
    
class ShowFollowing(ShowConnections):
    def get_template_context(self):
        context = dict()
        context['user_list'] = SubscriptionManager.get_following_users(self.profile_id_to_view,
                                                                       self.user_info['user_id'])
        context['following'] = True
        return context    
    
class ShowFollowers(ShowConnections):
    
    def get_template_context(self):
        context = {}
        context['user_list'] = SubscriptionManager.get_followers(self.profile_id_to_view, 
                                                                 self.user_info['user_id'])
        context['followers'] = True
        return context
    
class ShowEventsFromSubscription(BaseHandler):
    @user_required
    def get(self):
        context = self.get_template_context()
        context['events'] = context['events'][:15]
        context['subscription'] = True
        self.render_template('show_many_events.html', context)
    
    def get_template_context(self):
        filter_key = self.request.get('filter_key')
        sort_order = self.request.get('sort_order')
        tab = self.request.route_kwargs.get('page')
        context = {}
        context['left_sidebar'] = 'subscription'
        context['events'] = EventManager.get_events_from_subscription(self.user_info['user_id'], 
                                                                      category = tab, 
                                                                      filtered_by = filter_key, 
                                                                      ordered_by = sort_order)
        return context

class RpcSubscriptionGetEvents(ShowEventsFromSubscription, RpcMainGetEvents):
    @user_required
    def get(self, *args, **kargs):
        
        
        events = self.get_template_context()['events']
            
        self.prepare_and_serve_events(events)