#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

import logging
from google.appengine.api import mail
from market.handlers.base import BaseHandler
from shop.handlers.base_handler import RpcBaseHandler, user_required
from market.market_exceptions import UserNotFoundError


class VerificationHandler(BaseHandler):
    def get(self):
        signup_token = self.request.str_GET["signup_token"]
        verification_type = self.request.str_GET['type']
        user_id = self.request.str_GET['user_id']
        # it should be something more concise like
        # self.auth.get_user_by_token(user_id, signup_token
        # unfortunately the auth interface does not (yet) allow to manipulate
        # signup tokens concisely
        
        try:
            user = self.get_user_and_set_session(user_id, signup_token)
            
            if verification_type == 'v':
            # remove signup token, we don't want users to come back with an old link
                self.user_model.delete_signup_token(user.get_id(), signup_token)
                if user.type == 'student':
                    user.auth_ids.append(user.u_email)
                user.verify()
                
                self.redirect(self.uri_for('marketMain'))
            
            elif verification_type == 'p':
            # supply user to the page
                context = {
                'user': user,
                'token': signup_token
                }
                self.render_template('reset_password.html', context)
        
            else:
                logging.info('verification type not supported')
                self.abort(404)
        except UserNotFoundError:
            raise
    
    
    def get_user_and_set_session(self, user_id, signup_token):
        """
        Get the user specified by the user_id, and if found, set a session
        Else raise a user not Found error
        """
        user = self.user_model.get_by_auth_token(int(user_id), signup_token,
                                                 subject="signup"
                                                 )[0]
           
        if not user:
            
            logging.info('Could not find any user with id "%s" signup token'
             '"%s"', int(user_id), signup_token)
            
            raise UserNotFoundError('Could not find any user with id "%s" signup token'
             '"%s"'.format(int(user_id), signup_token))
            
        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), 
                              remember=True)
        return user

class RpcResendVerificationLink(RpcBaseHandler):
    @user_required
    def post(self):
        self.send_verification_link()
        self.send_success_response()
    def send_verification_link(self):
        """
        This function sends a verification email to the user whose user_id
        has been provided
        """
        user_id = self.user.key.id()
        token = self.user_model.create_signup_token(user_id)
        if self.user.type == 'student':
            email = self.user.u_email
            name = self.user.firstname
        else:
            email = self.user.email
            name = self.user.name
    
        verification_url = self.uri_for('marketVerification', type='v', user_id=user_id,
        signup_token=token, _full=True)
        
        logging.info(verification_url)
        
        message = mail.EmailMessage(sender="EventBuck Support <didia@eventbuck.com>",
                            subject="Bienvenue dans EventBuck")

        message.to = u"{0} <{1}>".format(name, email)
        
        message.body = \
        u"""
Cher {0}:

Vous pouvez confirmer votre addresse en cliquant sur le lien ci-dessous:
                       
{1}
                       
N'hesitez pas de nous contacter en cas des questions.

L'équipe d'EventBuck
        """.format(name, verification_url)

        message.send()
        