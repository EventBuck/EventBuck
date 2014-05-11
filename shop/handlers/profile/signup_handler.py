#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''
from google.appengine.api import mail

from shop.handlers.base_handler import BaseHandler

from shop.shop_exceptions import InvalidFormError, UserAlreadyExistError


class SignupHandler(BaseHandler):
    
    def get(self):
        
        self.render_template("signup.html", {'active': 'connexion'})
        
        
    def post(self):
        try:
            self.validate_form()
            posted_data = self.getRequiredPostedData()
            user=self.user_model.create_association(**posted_data)
            self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
            self.send_verifaction_email_to_user()
            self.redirect(self.uri_for('shopMain'))
        except InvalidFormError:
            raise
        except UserAlreadyExistError:
            raise
       
        
    def getRequiredPostedData(self):
        """
        This function allows us to get from posted data only data we need to use.
        """
        
        listOfNamesOfDataToClean = ['name', 'email', 'description', 'password', 'telephone']
        
        cleanedData = self.cleanPostedData(listOfNamesOfDataToClean)
        
        cleanedData['password_raw'] = cleanedData['password']
        
        #we delete the attribute password as required by for create_user method
        del cleanedData['password']

        
        return cleanedData
    
    def validate_form(self):
        list_of_required_data = ['name', 'email', 'password', 'confirm_email', 'confirm_password']
        
        is_form_valid = True
        message = ''
        
            
        
        try:
            super(SignupHandler, self).validate_form(list_of_required_data)
        except InvalidFormError as e:
            message += e.message + '\n'
            is_form_valid = False
        finally:
            if not mail.IsEmailValid(self.request.get('email')):
                is_form_valid = False
                message += 'The email you entered is invalid \n'
            if not self.request.get('email') == self.request.get('confirm_email'):
                is_form_valid = False
                message += 'The two emails didn\'t match \n'
            
            if not self.request.get('password') == self.request.get('confirm_password'):
                is_form_valid =False
                message += 'The two password didn\'t match \n'
           
            
            if not is_form_valid:
                raise InvalidFormError(message) 
            
       
    def send_verifaction_email_to_user(self):
        """
        This function sends a verification email to the user whose user_id
        has been provided
        """
        user_id = self.user.key.id()
        token = self.user_model.create_signup_token(user_id)
    
        verification_url = self.uri_for('marketVerification', type='v', user_id=user_id,
        signup_token=token, _full=True)
       
        message = mail.EmailMessage(sender="EventBuck Support <didia@eventbuck.com>",
                            subject="Bienvenue dans EventBuck")

        message.to = "{0} <{1}>".format(self.user.name, self.user.email)
        
        message.body = \
        """
        Cher {0}:

        Merci d'avoir rejoint EventBuck. EventBuck vous permettra d'être connecté à la grande communauté estudianstine de l'université Laval.
        Notre but est d'offrir aux étudiants de l'Université Laval une expérience inoubliable sur le campus comme à l'extérieur du campus.
        Nous sommes très ravis que vous ayez décidés de nous rejoindre pour atteindre cet objectif.
        Vous pouvez maintenant confirmer votre addresse en cliquant sur le lien ci-dessous:
                       
          {1}
                       
        N'hesitez pas de nous contacter en cas des questions.

        L'équipe d'EventBuck
        """.format(self.user.name, verification_url)

        message.send()
        
            
           
        
        