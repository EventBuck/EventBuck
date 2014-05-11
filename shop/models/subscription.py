#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 5 ao�t 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb

class Subscription(ndb.Model):
    """
    Class modeling an subscription
    """
    following = ndb.KeyProperty(required=True)
    approved = ndb.BooleanProperty(required=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)