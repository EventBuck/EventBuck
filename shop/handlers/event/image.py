#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2 juil. 2013

@author: Aristote Diasonama
'''



from .base import BaseHandler


class ImageHandler(BaseHandler):
    def get(self, *args, **kargs):
        
        if self.event.venue_picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(self.event.venue_picture)
        
                
        