'''
Created on 8 juin 2013

@author: macbookuser
'''

from .base_handler import BaseHandler

class TemplateViewer(BaseHandler):
    def get(self, template):
        template += '.html'
        self.render_template(template)

class ChannelViewer(BaseHandler):
    def get(self):
        self.render_template('channel.html')