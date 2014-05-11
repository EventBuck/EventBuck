#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 8 juin 2013

@author: macbookuser
'''

from .base import BaseHandler

class TemplateViewer(BaseHandler):
    def get(self, template):
        template += '.html'
        self.render_template(template)

class ChannelViewer(BaseHandler):
    def get(self):
        self.render_template('channel.html')