#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 28 oct. 2013

@author: Aristote Diasonama
'''
import logging
from sendgrid import Sendgrid
from message import Message
from admin import secure

s = Sendgrid(secure.SENDGRID_AUTH, secure.SENDGRID_PASS, secure = True)

def send(sender_name, sender, subject, text, html, receiver_email, receiver_name):
     
    subject = subject.encode('utf-8')
    text = text.encode('utf-8')
    html = html.encode('utf-8')
    receiver_name = receiver_name.encode('utf-8')
    sender_name = sender_name.encode('utf-8')
    message = None
     
    try:
        # update the <from_address> with your email address
            
        message = Message(sender_name, sender, subject, text=text, html=html)
        # add a recipient
            
    except Exception, msg:
        response = msg
        pass
            
    if message != None:
            # add a recipient
        try:
            message.set_replyto("support@eventbuck.com")
            message.add_to(receiver_email, receiver_name)
            message.add_header("Content-Type", "text/html; charset=UTF-8")
            message.add_header("X-Accept-Language", "fr")
        except Exception, msg:
            response = msg
            pass
        
        # use the Web API to send your message
        try:
            response = s.web.send(message)
        except Exception, msg:
            response = msg
            pass
        if response:
            logging.info("EMAIL SENT SUCCESSFULLY: {}".format(response))
        else:
            logging.error('FAILED TO SEND WEEKLY NOTIFICATIONS')