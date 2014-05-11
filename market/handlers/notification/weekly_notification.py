#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 29 sept. 2013

@author: Aristote Diasonama
'''

"""
Python Module handling daily notification sent to user about event taking place daily
"""
import logging

from market.handlers.main import MainHandler
from market.handlers.base import BaseHandler, jinja_environment
import memcache
from google.appengine.api import taskqueue

from shop.models.user  import EmailNotificationsSettings as NotifSettings
from market.lib.event import EventManager
from market.lib.event import UserManager
from vendors.sendgrid import sender

class StartWeeklyNotificationHandler(BaseHandler):
    """
    This class executes a cron job whose mere purpose is to add the
    CreateWeeklyNotificationHandler to the taskqueue
    """
    def get(self):
        weekly_events = EventManager.get_event_list(filtered_by='week')
        if weekly_events:
            taskqueue.add(url='/tasks/notification/weekly/start')
            
            
        self.render_template('ebdigest.html', {'event_list': weekly_events})
    
 
class CreateWeeklyNotificationHandler(BaseHandler):
    """
    This class create a list of task that the weekly notifier queue must execute
    """
    def post(self):
        task = self.add_task()
        if task:
            logging.info('TASK ADDED SUCCESSFULLY')
        else:
            logging.error('FAILED TO ADD TASK')
       
        
       
    def add_task(self):
        """
        add tasks for every users
        """
        user_email_dict = self.get_user_email_dict()
        if user_email_dict:
            for key in user_email_dict.keys():
                queue = taskqueue.Queue('weekly-notifier')
                task = queue.add(taskqueue.Task(url='/tasks/notification/weekly', 
                                      params={'user_id':key, 'email':user_email_dict[key]}))
        
            return task   
        
    
    def get_user_email_dict(self):
        """
        Get a dict of user_id as key and email to use to send notifications
        """


        users = UserManager.get_students()

        users_email_dict = {}
        
        if users:
            for user in users:
                
                user_notif = NotifSettings.get_settings_for(user_id=user['id'])
                if user_notif.weekly_digest:
                    users_email_dict[user['id']] = user_notif.email_to_use
            return users_email_dict
                
                
        
        
    
    

    
    
class SendWeeklyNotificationHandler(MainHandler):
    """
    This class will send daily notification to a user about the event he has to attend
    """
    def post(self):
        
        logging.info('SENDING EMAIL NOTIFICATION')
        user_id = int(self.request.get('user_id'))
        email = self.request.get('email')
        already_sent = memcache.get_weekly_sent_ids()
        
        if not user_id or not email:
            logging.debug('NO POST DATAS PROVIDED')
            return
        
        if user_id in already_sent:
            return
        
        user = UserManager.get_user_friendly(id=user_id)

        
        html_email = self.get_html_email(user)
        subject = self.get_subject(user)
        non_html_email = self.get_non_html_email(user)
        
        from main import debug
        if not debug:
            sender.send('EventBuck Notifications Hebdomadaire','digest-noreply@eventbuck.com', subject, text=non_html_email, html=html_email, 
                        receiver_email=email, receiver_name=user['fullname'])
            memcache.add_weekly_sent(user_id)
    
    def get_html_email(self, user):
        events = EventManager.get_event_list(filtered_by = 'week')
        return (jinja_environment.get_template('ebdigest.html').render({'event_list': events, 
                                                                       'user':user, 
                                                                       'subject':self.get_subject(user)
                                                                       }))
        
    def get_non_html_email(self, user):
        email = u"""
    {}, Visites ce lien pour voir les events qui auront lieu cette semaine sur EventBuck!
    
        www.eventbuck.com 
        
    """.format(user['firstname'])  
        
        return email
    
    def get_subject(self, user):
        return u"{}, À l'affiche cette semaine sur Eventbuck!".format(user['firstname'])
        
    