'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from google.appengine.ext import ndb

class Activity(ndb.Model):
    """
    Class which models an activity a user has done.
    
    :param type:
        an integer representing the type of the activity and tells what the activity is about
        We can have the following types:
        0.  joigned the site
        1.  created an event
        2.  added ticket to an event
        3.  modified an event
        4.  modified a ticket
        5.  published an event
        6.  deleted an event
        7.  deleted a ticket
        8.  going to an event 
        9.  cancelled attendance
        10. followed user
        11. unfollowed  user
        12. edited your profile
    :param target:
       this is a key of the targeted event or ticket involved in the modification
    :param date:
       the date the activity has been done. Automaticaly set when the instance is created
    
    """
    category = ndb.IntegerProperty(required=True, choices=[0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    target = ndb.KeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    def get_target_key(self):
        return self.target
    def get_category(self):
        return self.category
    def get_date(self):
        return self.date
    
    def get_activity_info(self):
        """
        this function returns the activity in string depending on its category
        """
        info_list = ["joigned the site", "added ticket to an event","created an event", "modified an event",
                        "modified a ticket", "published an event",
                        "deleted an event", "deleted a ticket of an event", "going to an event", "cancelled your attendance to the event",
                        "followed user", "unfollowed user", "edited your profile"]
        if self.category > len(info_list)-1:
            return "did this"
        return info_list[self.category]
    