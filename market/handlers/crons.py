#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 8 juil. 2013

@author: Aristote Diasonama
'''
import logging
import memcache
from .main import MainHandler


class UpdateMall(MainHandler):
    """
    This the handler used to update the mall object every 5 minutes
    """
    def get(self):
        if memcache.get_update_lock():
            return
        memcache.put_update_lock()
        logging.info('Cron jobs to update Mall started')
        mall = self.mall.get()
        updated = mall.update_mall()
        
        if updated == True:
            
            logging.info('Upcoming events updated successfully')
        else:
            logging.info('No updates found')
        memcache.delete_up_coming_events()
        memcache.remove_update_lock()   
        super(MainHandler, self).get()
        
    
    def post(self):
        self.get()
            
            
