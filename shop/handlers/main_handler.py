#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''
from django.utils import simplejson

from .base_handler import BaseHandler
from shop.shop_exceptions import NoActivitiesFoundError
from helper_functions import format_datetime

class MainHandler(BaseHandler):
   
    def get(self, *args, **kargs):
        print("IM IN SHOP")
        if self.user and not self.user.type == 'student' :
            try:
                
                context = self.get_home_context()
                self.render_template('home.html', context=context)
           
            except NoActivitiesFoundError:
                
                self.render_template('home.html', {'no_activities':True})
            
        else:
            if self.request.get('page') == 'about':
                self.render_template('about.html', {'active':'apropos'})
            
            else:
                self.render_template('index.html')
                
        self.redirect(self.uri_for('marketMain'))

    def get_activity_in_html(self, activity):
        
        target_id = activity.get_target_key().id()
        activity_format = 'You  <a href="{}">{} </a>'
        
        if activity.get_category() == 2:
            event_id = activity.get_target_key().parent().id()
            return activity_format.format(self.uri_for('showEvent',
                                                                  event_id = event_id),
                                          activity.get_activity_info())
                    
        if activity.get_category() == 4:
            return activity_format.format(self.uri_for('showTicket',
                                                                   event_id=target_id),
                                          activity.get_activity_info())  
        
        if activity.get_category() == 7:
            return activity_format.format(self.uri_for('showEvent'), activity.get_activity_info())
               
        else:
            return activity_format.format(self.uri_for('showEvent',
                                                                  event_id=target_id),
                                          activity.get_activity_info())
        

            
    def get_activities_formatted(self, start_cursor=None):
        results, cursor, more =  self.user.get_ten_activities(start_cursor)
        activities_date_and_html =zip(map(lambda result: format_datetime(result.get_date()), results), 
                                      map(self.get_activity_in_html, results))
        return(activities_date_and_html, cursor, more)
        
    def get_home_context(self, start_cursor=None):
        context  = dict()
        results, cursor, more = self.get_activities_formatted(start_cursor)

        activities_info = {'activities':results, 'cursor':cursor, 'more':more, 'url_to_load_more':self.uri_for('rpc_load_more')}
            
        context['activities_info'] = activities_info
            
        return context

            
class RpcLoadMoreActivities(MainHandler):
    
    def get(self, *args, **kargs):
        cursor = int(self.request.get('cursor'))
        context = self.get_home_context(start_cursor=cursor)
        print context
        self.send_success_response(context)
        
    def send_success_response(self, context):
        
        self.response.out.write(simplejson.dumps(context))
    
    def send_failed_response(self, message):
        pass            
 
        