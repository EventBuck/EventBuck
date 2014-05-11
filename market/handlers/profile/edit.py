#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 11 août 2013

@author: Aristote Diasonama
'''
from .signup import SignupHandler
from market.handlers.base import BaseHandler

from shop.handlers.base_handler import RpcBaseHandler
from shop.models.activity import Activity
from shop.shop_exceptions import RpcShopException
from helper_functions import get_full_major_name
import memcache
from shop.handlers.base_handler import user_required

class RpcEditFailedError(RpcShopException):
    """This exception is raised when Edit has failed
    """
    pass

class EditUserHandler(BaseHandler, SignupHandler):
    @user_required
    def get(self, *args,  **kargs):
        if self.request.route_kwargs.get('section') == 'password':
            self.render_template('password.html')
        elif self.request.route_kwargs.get('section') == 'notifications':
            notifications_settings = self.user.get_notifications_settings()
            
            self.render_template('email.html', {'notifications': notifications_settings})
        else:
            self.render_template('account.html')
    @user_required
    def post(self):
        user_key = self.edit_user()
        if user_key:
            self.log_this_activity(user_key)
            user =user_key.get()
            self.user = user
            memcache.set_user(user.key.id(), user)
        self.redirect(self.uri_for('viewUser', user_id=self.user_info['user_id']))
        
    def edit_user(self):
        posted_data = self.get_required_posted_data()
        return self.user.edit(posted_data)
        
    def log_this_activity(self, target):  
        self.user.log_activity(Activity(category=12, target=target)) 


class RpcEditUser(EditUserHandler, RpcBaseHandler):
    @user_required
    def post(self):
        try:
            user_key = self.edit_user()
            if user_key:
                self.log_this_activity(user_key)
                self.send_success_response()
                user =user_key.get()
                self.user = user
                memcache.set_user(user.key.id(), user)
            else:
                raise RpcEditFailedError
            
        except RpcEditFailedError as e:
            self.send_failed_response(e)
    
    def send_success_response(self):
        context = dict()
        context['picture'] = '<img src="{}" style="width:100%; height: 100%;"/>'.format(self.uri_for('userProfileImage', user_id=self.user.key.id()))
        try:
            context['description'] = self.user.description
        except AttributeError:
            pass
        
        if self.user.type == 'student':
            context['name'] = self.user.firstname + ' ' + self.user.name
            try:
                context['major'] = get_full_major_name(self.user.major)
            except AttributeError:
                pass
        else:
            context['name'] = self.user.name
        
        super(RpcEditUser, self).send_success_response(context)

class RpcEditNotification(RpcEditUser):
    @user_required
    def post(self):
        try:
            user_key = self.edit_notification_settings()
            if user_key:
                self.log_this_activity(user_key)
                self.send_success_response()
            else:
                raise RpcEditFailedError
        except RpcEditFailedError as e:
            self.send_failed_response(e)
    
    def edit_notification_settings(self):
        data = self.get_notifications_data()
        return self.user.edit_notifications_settings(data)
    
    def get_notifications_data(self):
        list_of_data = ['email_to_use', 'daily_alert', 'weekly_digest', 'newsletter', 'help_me'] 
    
        posted_data = self.cleanPostedData(list_of_data)
        
        
        for name in list_of_data[1:]: # because we don't need a boolean for contact-email
            posted_data[name] = True if posted_data.get(name) else False
        if posted_data.get('email_to_use'):
            if not posted_data['email_to_use'] == 'email' and not posted_data['email_to_use'] == 'u_email':
                del posted_data['email_to_use']
        return posted_data