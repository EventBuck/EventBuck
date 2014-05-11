#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 23 ao�t 2013

@author: Aristote Diasonama
'''

from google.appengine.api import mail
from shop.handlers.base_handler import RpcBaseHandler


class Contact(RpcBaseHandler):
    def post(self):
        pass
    def send_message_to_support(self):
        """
        This function sends the posted message to the support team
        """
        
        message_info = self.get_required_posted_data()
        
        if self.user:
            message_info['category'] = 'Existing User'
            
        
        message = mail.EmailMessage(sender="EventBuck Support <support@eventbuck.com>",
                            subject="Bienvenue dans EventBuck")

        message.to = "{0} <{1}>".format('EventBuck Support', 'support@eventbuck.com')
        
        message.body = \
        """Cher {0}:

           Merci d'avoir rejoint la grande communauté des étudiants actifs de l'université Laval.  Vous pouvez confirmer
           votre adesse en cliquant sur le lien ci-dessous:
                       
           {1}
                       
           N'hesitez pas de nous contacter en cas des questions

           L'équipe d'EventBuck
        """.format(self.user.firstname)

        message.send()
    def get_required_posted_data(self):
        list_of_datas_to_clean = ['firstname', 'name', 'email', 'subject', 'description', 'category']
        cleaned_data = self.cleanPostedData(list_of_datas_to_clean)
        return cleaned_data