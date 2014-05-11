'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb

from .user import User
from .ticket import Ticket


class Achat(ndb.Model):
    """
    Class modeling an achat made by a user.
    This class is supposed to model all the achat made through this application
    This will be the child of an class Ticket
    """
    buyer = ndb.KeyProperty(kind=User, required=True)
    ticket = ndb.KeyProperty(kind=Ticket, required=True)
    ip_buyer = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)

        