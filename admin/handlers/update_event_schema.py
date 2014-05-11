#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 10 sept. 2013

@author: Aristote Diasonama
'''

import logging
from shop.models import event
from google.appengine.ext import deferred
from google.appengine.ext import ndb

BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

def UpdateSchema(cursor=None, num_updated=0):
    query = event.Event.query()
    if cursor:
        query.with_cursor(cursor)

    to_put = []
    for e in query.fetch(limit=BATCH_SIZE):
       
        #delete the attribute venue_picture
        
        to_put.append(e)

    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.debug(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
        deferred.defer(
            UpdateSchema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with %d updates!', num_updated)