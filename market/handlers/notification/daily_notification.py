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
from vendors.sendgrid import sender
import memcache
from market.handlers.base import BaseHandler, jinja_environment
from market.handlers.main import MainHandler
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from market.lib.event import EventManager
from market.lib.user import UserManager
from market.lib.attendance import AttendanceManager


from shop.models.user  import EmailNotificationsSettings as NotifSettings


class StartDailyNotificationHandler(BaseHandler):
    """
    This class executes a cron job whose mere purpose is to add the
    CreateWeeklyNotificationHandler to the taskqueue
    """
    def get(self):
        today_events = EventManager.get_event_list(filtered_by = 'today')
        if today_events:
            task = taskqueue.add(url='/tasks/notification/daily/start')
        self.render_template('ebdigest.html', {'event_list': today_events})
   

class CreateDailyNotificationHandler(BaseHandler):
    """
    This class create a list of task that the daily notifier queue must execute
    """
    def post(self):
        self.add_task()
        events = EventManager.get_event_list(filtered_by='today')
        self.render_template('ebdigest.html', {'event_list': events})
       
    def add_task(self):
        """
        add tasks to the given event
        """
        user_event_dict = self.get_user_event_dict()
        if user_event_dict:
            for user_id in user_event_dict.keys():
                queue = taskqueue.Queue('daily-notifier')
                queue.add(taskqueue.Task(url='/tasks/notification/daily', 
                          params={'user_id':user_id, 
                                  'email':user_event_dict[user_id]['email'],
                                  'events':user_event_dict[user_id]['events']
                                  }))
             
        
    
    def get_user_event_dict(self):
        """
        Get a dict of user_id as key and dict of list of events they are attending today and their email as value
        """
        events = EventManager.get_event_list(filtered_by='today')
        user_event_dict = {}
        already_in_dict = []
        no_send = []
        
        for event in events:
            event_key = ndb.Key(urlsafe=event['key'])
            user_ids = AttendanceManager.get_users_id_attending(event_key)
            if user_ids:
                for an_id in user_ids:
                    if an_id in already_in_dict:
                        user_event_dict[an_id]['events'].append(event['key'])
                    else:
                        if not an_id in no_send:
                            user_notif = NotifSettings.get_settings_for(user_id=an_id)
                            if user_notif.daily_alert:
                                user_event_dict[an_id] = {}
                                user_event_dict[an_id]['email'] = user_notif.email_to_use
                                user_event_dict[an_id]['events'] = [event['key']]
                                already_in_dict.append(an_id)
                            else:
                                no_send.append(an_id)    
                
        
        return user_event_dict
    
class SendDailyNotificationHandler(MainHandler):
    """
    This class will send daily notification to a user about the event he has to attend
    """
    def post(self):
        user_id = int(self.request.get('user_id'))
        event_keys = self.request.get('events', allow_multiple=True)
        email = self.request.get('email')
        
        already_sent = memcache.get_daily_sent_ids()
        
        if not user_id or not email:
            logging.debug('NO POST DATAS PROVIDED')
            return
        
        if user_id in already_sent:
            return
        
        events = filter(lambda event: event['key'] in event_keys, EventManager.get_event_list(filtered_by='today'))
        print(events)
        user = UserManager.get_user_friendly(id =user_id)
        
        if not user_id or not email:
            logging.debug('NO POST DATAS PROVIDED')
            return
        html_email = self.get_html_email(user, events)
        subject = self.get_subject(user)
        non_html_email = self.get_non_html_email(user)
        
        from main import debug
        if not debug:
            sender.send('EventBuck Rappel','reminder@eventbuck.com', subject, text=non_html_email, html=html_email, 
                        receiver_email=email, receiver_name=user['fullname'])
            memcache.add_daily_sent(user_id)
        
    def get_html_email(self, user, events):
        return jinja_environment.get_template('ebdigest.html').render({'event_list': events, 
                                                                       'user':user,
                                                                       'subject':self.get_subject(user)
                                                                       })  
    def get_non_html_email(self, user):

        email = u"""
    {}, Visites ce lien pour voir les events qui auront lieu cette semaine sur EventBuck!
    
        www.eventbuck.com 

    """.format(user['firstname'] if user['type']=='student' else user['fullname'])  
        
        return email
    def get_subject(self, user):
        return u"{}, Rappel des events à participer!".format(user['firstname'] if user['type']=='student' else user['fullname'])