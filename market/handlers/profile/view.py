#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import webapp2
from market.handlers.base import BaseHandler
import memcache
from market.lib.subscription import SubscriptionManager
from market.lib.event import EventManager

from shop.handlers.base_handler import user_required




class ViewProfileHandler(BaseHandler):
    @webapp2.cached_property
    def profile_id_to_view(self):
        if self.request.route_kwargs.get('user_id'):
            return int(self.request.route_kwargs.get('user_id'))
        else:
            return self.user_info['user_id']
    @user_required
    def get(self, *args, **kargs):
        
        context = self.get_template_context()
        self.render_template('user.html', context=context)
        
    def get_template_context(self):
        
        context = dict()
        context.update(self._get_profile_info())
        if context['target']['type']  == 'student':
            context['events_by_user'], context['events_by_others'] = self._get_events_by_user_and_by_other()
        else:
            context['events_by_user'] = EventManager.get_events_by(self.profile_id_to_view)
        
        
        return context
    def _get_profile_info(self):
        """Return a dict with profile information
        """
        context = dict()
        user = SubscriptionManager.get_marked_user(user_id=self.profile_id_to_view, current_user_id=self.user_info['user_id'])
        context['target'] = user

        context['following_number'], context['followers_number'] = SubscriptionManager.get_user_stats(self.profile_id_to_view)
        
        
        return context
    
    
    
    
    def _get_events_by_user_and_by_other(self):
        """
        Return a tuple of two lists, the first being
        events by user and the second events by others
        """
        events = EventManager.get_events_attending(user_id=self.profile_id_to_view)

        by_user = []
        by_others = []
        for event in events:
            if event['seller_id'] == self.profile_id_to_view:
                by_user.append(event)
            else:
                by_others.append(event)

        return by_user, by_others
    
   
              
        
    def _get_user_subscription_stats(self):       
        """
        Get user subscriptions stats
        return a tuple of two integers, one representing following and second followers
        """
        following = memcache.get_following_number(self.profile_id_to_view)
        followers = memcache.get_followers_number(self.profile_id_to_view)
        
        
        return following, followers
        