'''
Created on 29 juin 2013

@author: macbookuser
'''


from shop.handlers.base_handler import BaseHandler
from shop.handlers.base_handler import user_required
from google.appengine.ext import db
from google.appengine.api import images

class ProfileImageHandler(BaseHandler):
    @user_required
    def get(self):
        if self.user.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(self.user.picture)
        else:
            self.response.out.write('shop/static/img/logo1.png')
            
    @user_required
    def post(self):
        try:
            avatar = images.resize(self.request.get('img'), 300)
            self.user.picture = db.Blob(avatar)
            self.user.put()
        finally:
            self.response.out.write('<img src="{}" style="width:120px; height: 80px;"/>'.format(self.uri_for('profilePicture')))
        
        