#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''


import logging
from google.appengine.api import mail
from shop.shop_exceptions import UserNotFoundError
from shop.handlers.base_handler import RpcBaseHandler

class RpcForgotPasswordHandler(RpcBaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        try:
            self._get_user_and_send_reset_link()
            self.send_success_response()
        except UserNotFoundError as e:
            self.send_failed_response(error=e)
    def _get_user_and_send_reset_link(self):
        posted_data = self.cleanPostedData(['email'])
        email = posted_data.get('email')

        user = self.user_model.get_by_auth_id(email)
        if not user:
            logging.info('Could not find any user entry for email %s', email)
            raise UserNotFoundError('A user with the given email doesn\'t exist')
            
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('marketVerification', type='p', user_id=user_id,
          signup_token=token, _full=True)

        logging.info(verification_url)
        
        message = mail.EmailMessage(sender="EventBuck Support <didia@eventbuck.com>",
                            subject="Bienvenue dans EventBuck")

        message.to = "{0} <{1}>".format(user.get_full_name(), email)
        
        message.body = \
        """
Cher {0}:
Nous avons réçu votre requête d'oubli de mot passe.

Vous pouvez créer un nouveau mot de passe en suivant le lien ci-dessous:
                       
        {1}
Si vous n'êtes pas à l'origine de cette requête, pas de panique, ignorez ce message et votre mot de passe ne sera pas changé.                 


N'hesitez pas de nous contacter en cas des questions.

        L'équipe d'EventBuck
        """.format(user.get_full_name(), verification_url)

        message.send()
        
  

        