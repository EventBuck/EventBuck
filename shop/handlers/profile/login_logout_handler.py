#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import logging
from shop.handlers.base_handler import BaseHandler, no_user_required
import helper_functions as helpers

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError


class LoginHandler(BaseHandler):
    @no_user_required
    def get(self):
          
        self.render_template('signin.html', {'active':'connexion'})
    @no_user_required
    def post(self):
        posted_data = self.cleanPostedData(['email', 'password', 'remember_me'])
        username = posted_data.get('email')
        password = posted_data.get('password')
        if posted_data.get('remember_me'):
            remember = True
        else:
            remember = False
        try:
            self.auth.get_user_by_password(username, password, remember=remember,
                save_session=True)
            callback = self.request.get('callback');
            if callback and helpers.is_good_callback(callback, self.request.host_url):
                self.redirect(str(callback))
            else:
                
                self.redirect(self.uri_for('marketMain'))
                
            
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', username, type(e))
            self.redirect(self.uri_for('marketAuthenticate', d=1))


class LogoutHandler(BaseHandler):
    
    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('shopMain'))

