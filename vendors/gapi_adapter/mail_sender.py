#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 5 nov. 2013

@author: Aristote Diasonama
'''


from google.appengine.api import mail

def send(sender, subject, text, html, receiver_email, receiver_name):
    
    message = mail.EmailMessage(sender=sender,
                            subject=subject, to="{0} {1}".format(receiver_name, receiver_email),
                            body=text, html=html)
    message.send()
    
