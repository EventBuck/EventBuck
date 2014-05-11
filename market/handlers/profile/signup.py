#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''


from google.appengine.api import mail
from shop.handlers.base_handler import BaseHandler, no_user_required, RpcBaseHandler
import logging
from shop.shop_exceptions import InvalidFormError, UserAlreadyExistError
from helper_functions import is_valid_ul_email, is_good_callback
import facebook
from admin.secure import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from market.handlers.main import MainHandler
from google.appengine.ext import db
from google.appengine.api import images
from market.lib.user import UserManager


class SignupHandler(BaseHandler):
    
    def post(self):
        try:
            self.validate_and_signup_user()
            
            self.redirect(self.uri_for('marketMain'))
        except InvalidFormError:
            raise
        except UserAlreadyExistError:
            raise
    def validate_and_signup_user(self):
        self.validate_form()
        posted_data = self.get_required_posted_data()
        user=UserManager.create_student(posted_data)
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        self.send_verifaction_email_to_user()
    
    def get_required_posted_data(self):
        """
        This function allows us to get from posted data only data we need to use.
        """
        
        listOfNamesOfDataToClean = ['firstname', 'name', 'email', 'password', 'u_email', 'gender', 'description', 'major']
        
        cleanedData = self.cleanPostedData(listOfNamesOfDataToClean)
        
        if not cleanedData.get('gender'):
            cleanedData['gender'] = 'male'
        
        if cleanedData.get('password'):
            cleanedData['password_raw'] = cleanedData['password']
        
            #we delete the attribute password as required by for create_user method
            del cleanedData['password']
        if self.request.get('picture'):
            cleanedData['picture'] = self.request.get('picture')
        return cleanedData
    
    def validate_form(self):
        list_of_required_data = ['firstname', 'name', 'email', 'u_email', 'password', 'gender']
        
        is_form_valid = True
        message = ''
        
            
        
        try:
            super(SignupHandler, self).validate_form(list_of_required_data)
        except InvalidFormError as e:
            message += e.message + '\n'
            is_form_valid = False
        finally:
            
            if not mail.is_email_valid(self.request.get('email')) or not mail.is_email_valid(self.request.get('u_email')):
                is_form_valid = False
                message += 'One of the email you entered is not valid \n'
            if not is_valid_ul_email(self.request.get('u_email')):
                is_form_valid = False
                message += 'The UL email entered is not valid'
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

        message.to = u"{0} <{1}>".format(self.user.firstname, self.user.u_email)
        
        message.body = \
        u"""
Cher {0}:

Merci d'avoir rejoint la grande communauté des étudiants actifs de l'Université Laval. 
EventBuck vous permettra de rester informé sur les events organisés à l'intention des étudiants. Notre Objectif est de rendre l'expérience sur le campus inoubliable pour  
tous les étudiants en leur permettant de profiter complètement de ce  qu'offre l'université Laval en termes d'events, tant du point de vue académique que para-académique.
Vous pouvez maintenant confirmer votre adresse en cliquant sur le lien  
ci-dessous:
                       
          {1}
                       
N'hesitez pas de nous contacter si vous avez des questions.

L'équipe d'EventBuck
        """.format(self.user.firstname, verification_url)

        message.send()
        
class RpcSignupHandler(RpcBaseHandler, SignupHandler):
    def post(self):
        try:
            self.validate_and_signup_user()
            print(self.request.get('callback'))
            if(self.request.get('callback') and is_good_callback(self.request.get('callback'), self.request.host_url)):   
                self.send_success_response({'redirect':True})
            else:
                self.send_success_response({'redirect':False})
        except InvalidFormError as e:
            self.send_failed_response(error=e)
        except UserAlreadyExistError as e:
            self.send_failed_response(error=e)
        finally:
            print("host : " + self.request.host_url + " " +self.request.get('callback') +" status: "+ str(is_good_callback(self.request.get('callback'), self.request.host_url)))


            
        
    
        
            

class FacebookSignup(MainHandler, SignupHandler): 
    @no_user_required
    def get(self):
        callback = self.request.get('callback')
        try:
            cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:


                logging.info(cookie)

                firstname = cookie.get("first_name")

                user = self.user_model.get_by_fb_id(cookie["uid"])
                if user:
                    self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
                    if callback and is_good_callback(callback):
                        self.redirect(str(callback))
                    self.redirect(self.uri_for("marketMain"))
                else:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = self.user_model.get_by_auth_id(profile["email"])
                    if user:
                        profile['access_token'] = graph.extend_access_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)['access_token']
                        user.edit({'facebook_link':profile['link'], 'fb_access_token':profile['access_token'], 'fb_id':profile['id']})
                        self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
                        self.redirect(self.uri_for("marketMain"))
                    else:
                        self.render_template('facebook_signup_landing.html', {'first_name':firstname, 'callback':callback})
            else:        
               
                self.render_template('facebook_signup_landing.html', {'callback': callback})
                
        except facebook.GraphAPIError as e:
            logging.info(e)
            self.render_template('facebook_signup_landing.html', {'callback':callback})
            
        
    @no_user_required
    def post(self):
        self.validate_form()
        posted_data = self.get_required_posted_data()
        
        try:

            access_token = self.get_fb_access_token()      

            if not access_token:
                self.redirect("//www.facebook.com/dialog/oauth?client_id=129359370579954&\
            redirect_uri=http%3A%2F%2Fwww.eventbuck.com%2Fsignup%2Ffb&response_type=token&scope=email,publish_actions")
        
    
            posted_data.update(self.get_all_required_data_from_fb(access_token))
            self.get_or_create_user(posted_data)
                
        
        except facebook.GraphAPIError as e:

            logging.info(access_token)


            logging.info(e)
            self.redirect("//www.facebook.com/dialog/oauth?client_id=129359370579954&\
            redirect_uri=http%3A%2F%2Fwww.eventbuck.com%2Fsignup%2Ffb&response_type=token&scope=email,publish_actions")
                
              
        
        
    def validate_form(self):
        list_of_required_data = [ 'u_email', 'password', 'gender']
        is_form_valid = True
        message = ''
        
        try:
            super(SignupHandler, self).validate_form(list_of_required_data)
        except InvalidFormError as e:
            message += e.message + '\n'
            is_form_valid = False
        finally:
            if not (mail.is_email_valid(self.request.get('u_email'))):
                is_form_valid = False
                message += 'One of the email you entered is not valid \n'
            if not is_valid_ul_email(self.request.get('u_email')):
                is_form_valid = False
                message += 'The UL email entered is not valid'
            if not self.request.get('password') == self.request.get('confirm_password'):
                is_form_valid =False
                message += 'The two password didn\'t match \n'
            
            if not is_form_valid:
                raise InvalidFormError(message) 
    
    def get_fb_access_token(self):
        """Get facebook access token
        """
        cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
        if cookie:
            access_token = cookie["access_token"]
        else:
            access_token = self.request.get('access_token')
        return access_token
    
    def get_all_required_data_from_fb(self, access_token):
        """
        Given the access token, get all the data we need from facebook and return it as a dict
        """
        facebook_data = dict()
        graph = facebook.GraphAPI(access_token) 
        profile = graph.get_object("me")
        data_from_facebook = {'email':'email','firstname':'first_name', 'name':'last_name', 'facebook_link':'link', 'fb_id':'id', 'gender':'gender'}
        for key in data_from_facebook.keys():
            facebook_data[key] = profile[data_from_facebook[key]]
        
        path_picture = profile["id"] + "/picture"
        image = graph.get_object(path_picture, type="large")["data"]
        avatar = images.resize(image, 300)
        picture = db.Blob(avatar)
        facebook_data['picture'] = picture
        facebook_data['fb_access_token'] = graph.extend_access_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)['access_token']
        
        return facebook_data
    
    def get_or_create_user(self, posted_data):
        """
        This session checks if the user with the facebook info already exists.
        If he exists, we update his facebook details and start a new session
        Else we create a new user and start a session for him
        """
        user = self.user_model.get_by_fb_id(posted_data["fb_id"])
        if user:
            self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        else:
            try:
                user=UserManager.create_student(posted_data)
                self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
                self.send_verifaction_email_to_user()
             
            except UserAlreadyExistError:
                user = self.user_model.get_by_auth_id(posted_data["email"])
                if not user:
                    raise UserAlreadyExistError('A user with the u_email provided already exists')
                user.edit({'facebook_link':posted_data['facebook_link'], 'fb_access_token':posted_data['fb_access_token'], 'fb_id':posted_data['fb_id']})
                self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        
         

class RpcFacebookSignup(RpcBaseHandler, FacebookSignup):
    def post(self):
        try:
            self.validate_form()
            posted_data = self.get_required_posted_data()
            access_token = self.get_fb_access_token()
            posted_data.update(self.get_all_required_data_from_fb(access_token))
            self.get_or_create_user(posted_data)
            if(self.request.get('callback') and is_good_callback(self.request.get('callback'), self.request.host_url)):
                self.send_success_response({'redirect':True})
            else:
                self.send_success_response({'redirect':False})
        except InvalidFormError as e:
            self.send_failed_response(error=e)
        except UserAlreadyExistError as e:
            self.send_failed_response(error=e)
        except facebook.GraphAPIError as e:
            self.abort(403)
            
    
            