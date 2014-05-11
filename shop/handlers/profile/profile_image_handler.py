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
    def get(self, *args, **kargs):
        user_id = self.request.route_kwargs.get('user_id')
        if user_id:
            user = self.user_model.get_by_id(int(user_id))
        else:
            user = self.user.key.get()
        if user.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user.picture)
        else:
            self.response.out.write('shop/static/img/logo1.png')
            
    @user_required
    def post(self):
        try:
            avatar = images.resize(self.request.get('img'), 300)
            self.user.picture = db.Blob(avatar)
            print(self.user.put())
        finally:
            self.response.out.write('<img src="{}" style="width:100%; height: 100%;"/>'.format(self.uri_for('userProfileImage', user_id=self.user.key.id())))
        
        