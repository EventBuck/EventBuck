#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 14 sept. 2013

@author: Aristote Diasonama
"""
from shop.handlers.base_handler import RpcBaseHandler

from market.handlers.base import BaseHandler

from market.lib.user import UserManager
from market.lib.subscription import SubscriptionManager


class ShowCommunityHandler(BaseHandler):
    def get(self, *args, **kargs):
        page = self.request.route_kwargs.get('page')
        context = self.get_template_context(page)
        if self.user:
            context['user_list'] = context['user_list'][:15]
        context['active'] = 'community'
        self.render_template('community.html', context)
    def get_template_context(self, page):
        context = dict()
        if page == 'asso':
            user_list = UserManager.get_asso()
            context['sub_active'] = 'asso'
        else:
            user_list = UserManager.get_students()
            context['sub_active'] = 'people'
        
        if self.user:
            SubscriptionManager.mark_users(user_list, self.user_info['user_id'])
        
        context['user_list'] = user_list
        
        return context  

class RpcShowCommunityHandler(ShowCommunityHandler, RpcBaseHandler):
    def get(self, *args, **kargs):
        
        page = self.request.route_kwargs.get('page')
        users = self.get_template_context(page)['user_list']
        self.prepare_and_serve_users(users)
        
        
       
    def prepare_and_serve_users(self, users):
        cursor = self.request.get('cursor')
     
        if cursor:
            cursor = int(cursor)
            new_cursor = cursor + 15
            if len(users[cursor:]) > 15:
                more = True
            else:
                more = False
            users = users[cursor:new_cursor]
        else:
            if len(users) > 15:
                more = True
            else:
                more = False
            users = users[:15]
            new_cursor = 15
        
    
        response = {'users':users, 'cursor':new_cursor, 'more':more}
        
        self.send_success_response(response)
              
        

    
   
        
       

