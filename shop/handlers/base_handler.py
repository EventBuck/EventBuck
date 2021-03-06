#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: macbookuser
'''

import logging
from xml.sax.saxutils import escape
from django.utils import simplejson

from google.appengine.ext import ndb


import webapp2
import jinja2

from webapp2_extras import auth
from webapp2_extras import sessions

from shop.shop_exceptions import InvalidFormError

import helper_functions as helpers





jinja_environment = jinja2.Environment(extensions=['jinja2.ext.autoescape'],
    loader=jinja2.PackageLoader('shop', 'templates'))

jinja_environment.filters['check_active'] = helpers.check_active
jinja_environment.filters['datetime'] = helpers.format_from_timestamp
jinja_environment.filters['datetime_to_jquery'] = helpers.inverse_jquery_datepicker_parser







def asso_required(handler):
    """
    Decorator that checks if there's a association associated with the current session.
    Will also fail if there's no session present.
    """
    def check_login(self, *args, **kargs):
        auth = self.auth
        user = auth.get_user_by_session()
        if not user:
            self.redirect(self.uri_for('marketAuthenticate', callback=self.request.url))
        else:
            if self.user.type == 'student':
                return self.redirect(self.uri_for('marketMain'))
                
            else:
                return handler(self, *args, **kargs)

    return check_login

def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    """
    def check_login(self, *args, **kargs):
        auth = self.auth
        user = auth.get_user_by_session()
        if not user:
            self.redirect(self.uri_for('marketAuthenticate', callback=self.request.url))
        else:
            return handler(self, *args, **kargs)
            
        
    return check_login

def no_user_required(handler):
    """
    This decorator is the opposite of user_required.
    Will fail if there is a session
    """
    def check_login(self, *args, **kargs):
        auth = self.auth
        user = auth.get_user_by_session()
        if not user:
            return handler(self, *args, **kargs)
        else:
            self.redirect(self.uri_for('marketMain'))
           
        
    return check_login

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def key(self):
        """Shortcut to access the datastore key of the user model
        """
        return ndb.Key(self.user.key.kind(), self.user.key.id()) if self.user_info else None
    @webapp2.cached_property
    def gparams(self):
        """Shortcut to access all default parameters that must be present in all templates
        """
        params = {'url_for_signup':webapp2.uri_for('shopSignUp'), 'url_for_signin':webapp2.uri_for('shopLogin'),
                'url_for_logout':webapp2.uri_for('shopLogout'), 'url_for_createEvent':webapp2.uri_for('createEvent'),
                'url_for_showEvent':webapp2.uri_for('showEvent'),
                'url_for_index': webapp2.uri_for('shopMain'), 'active':"home",
                'sidebar_active':"newsfeed", 'url_for_about':webapp2.uri_for('shopMain', page='about'),
                'profile_picture': self.get_profile_picture_url(), 
                'url_for_profile_picture':webapp2.uri_for('profilePicture')}
        return params
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property.
           Also check if a facebook session is in place, if yes, set the session"""

        """

        cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
        if cookie:
            logging.info("COOKIE TROUVE")
            user = self.user_model.get_by_fb_id(cookie["uid"])
            if user:
                self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        """

        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
           in the session.

           The list of attributes to store in the session is specified in
           config['webapp2_extras.auth']['user_attributes'].
           :returns
            A dictionary with most user information
        """
        return self.auth.get_user_by_session()
        
            

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
          The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        if u:
            user = self.user_model.get_by_id(u['user_id'])
            
            return user
            
        return None
            

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """    
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, context=None):
        
        params = dict(self.gparams)
        if not context is None:
            params.update(context)
            
        params['user'] = self.user
        if self.user:
            params['j_user'] = simplejson.dumps(self.user.get_user_in_dict())
        
        jtemplate = jinja_environment.get_template(view_filename)
        self.response.out.write(jtemplate.render(params))
    
    def get_profile_picture_url(self):
        if self.user:
            if self.user.picture:
                return webapp2.uri_for('profilePicture')
        return '/shop/static/img/logo1.png'
    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
          'message': message
        }
        jtemplate = jinja_environment.get_template('message.html')
        self.response.out.write(jtemplate.render(params))

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    def handle_exception(self, exception, debug):
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        self.response.write(exception)

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
            
    def cleanPostedData(self, listOfNamesOfDataToClean):
        """
        Function to clean arguments from html markups 
        
        :param properties:
            A list of arguments name we must clean
        :return edited_values:
            Dict that will contain the cleaned values
        """
        edited_values = {}
        for value in listOfNamesOfDataToClean:
                if self.request.get(value):
                    edited_values[value] = escape(self.request.get(value))
        return edited_values
   
    def validate_form(self, list_of_required_data_names):
        """
        Function to validate form data. This function checks if all required
        data have been provided.
        """
        is_form_valid = True
        field_missing_value =[]
        for name in list_of_required_data_names:
            if self.request.get(name) is None:
                if is_form_valid:
                    is_form_valid = False
                field_missing_value.append(name)
        
        
        
        if not is_form_valid:
            message = "You must fill fields "+ ' '.join(field_missing_value)
            raise InvalidFormError(message)
                
            

class RpcBaseHandler(BaseHandler):
         
    def send_success_response(self, message='success'):
        
        self.response.out.write(simplejson.dumps(message))
    def send_failed_response(self, error=None, message="error"):
        if not error is None:
            logging.error(unicode(error.message))
            self.response.out.write(simplejson.dumps(error.message))
            self.response.set_status(error.code)
        else:
            logging.error(message)
            self.response.out.write(simplejson.dumps(message))
            self.response.set_status(500)
            
