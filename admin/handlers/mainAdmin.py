
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from market.handlers.base import BaseHandler
from django.utils import simplejson
from market.lib.event import EventManager

'''
Created on 8 févr. 2014
'''

class MainAdminHandler(BaseHandler):
    def get(self):
        
        upcoming_events = EventManager.get_upcoming_events()
        
        self.render_template('admin.html', {'events': 'test'})

