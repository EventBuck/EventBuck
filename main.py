'''
Created on 15 mars 2013

@author: Aristote Diasonama
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-


import webapp2
import os
from router import applications_routes
from admin import secure

__all__ = ['debug', 'config']

if os.environ['SERVER_SOFTWARE'].find('Development') == 0:
    debug = True
else:
    debug = False











config = {
  'webapp2_extras.auth': {
    'user_model': 'shop.models.user.User',
    'user_attributes': ['name', 'type','verified'],
    #'session_backend': 'datastore'
    'session_backend': 'memcache'
  },
  'webapp2_extras.sessions': {
    'secret_key': secure.APP_SECRET,
    'backends':{'datastore': 'webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory',
                 'memcache': 'webapp2_extras.appengine.sessions_memcache.MemcacheSessionFactory',
                 'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory' 
}
  }
}




app = webapp2.WSGIApplication(routes=applications_routes,
                               config=config,
                              debug=debug)
