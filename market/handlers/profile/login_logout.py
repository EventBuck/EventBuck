#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''


from market.handlers.base import BaseHandler
from shop.handlers.profile.login_logout_handler import LoginHandler as ShopLogin
from shop.handlers.base_handler import no_user_required


class LoginHandler(BaseHandler, ShopLogin):
    @no_user_required
    def get(self):
        self.render_template('signin.html', {'active':'login', 'callback':self.request.get('callback')})


class LogoutHandler(BaseHandler):
    
    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('marketMain'))

class Authenticate(LoginHandler):
    @no_user_required
    def get(self):
        context = {'callback':self.request.get('callback')}
        if self.request.get('d'):
            context = {'message': u"L'email ou le mot de passe entré n'est pas valide, Réessayez svp!"}
        self.render_template('authenticate.html', context)
