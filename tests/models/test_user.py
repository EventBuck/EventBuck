
'''
Created on 6 juin 2013

@author: macbookuser
'''
import unittest
import datetime
from tests.test_utils import OjoTest
from shop.models.user import User
from shop.models.activity import Activity

from shop.shop_exceptions import UserAlreadyExistError

name = "test1"
email = "aristotediasonama@yahoo.fr"
u_email = "aristotediasonama@ulaval.ca"
venue_name = "place1"
venue_addresse = "place5"
description = "description"
date_event = datetime.datetime.now()
class TestUser(OjoTest):
    
    def setUp(self):
        super(TestUser, self).setUp()
        self.association = User.create_association(name=name, email=email)
        self.user = User.create_student(name=name, email="jake@gmail.com", u_email=u_email)

    def test_create_association_valide(self):
        """ here we test valid cases, an exception must not be raised
        """
        
        try:
            User.create_association(name=name, 
                                            email="thefuture2092@gmail.com")
        except UserAlreadyExistError:
            self.fail("the exception has been raised while a unique user was\
             indeed created")
            
    def test_create_association_invalide(self):
        """
        Here we test when a duplicated user is created, ie same email, an \
        exception must be raised
        """
        
        self.assertRaises(UserAlreadyExistError,User.create_association
                          ,name=name, email=email)
        
        self.assertRaises(UserAlreadyExistError,User.create_association
                          ,name="test2", email=email)
        
    
    def test_create_student_valide(self):
        """ here we test valid cases, an exception must not be raised
        """
        
        try:
            User.create_student(name=name, 
                                            email="test@gmail.com", u_email="kevin@ulaval.ca")
        except UserAlreadyExistError:
            self.fail("the exception has been raised while a unique user was\
             indeed created")

    
    def test_create_student_invalide(self):
        """
        Here we test when a duplicated user is created, ie same email, an \
        exception must be raised
        """
        
        self.assertRaises(UserAlreadyExistError,User.create_student
                          ,name=name, email=email, u_email = "test@ulaval.ca")
        
        self.assertRaises(UserAlreadyExistError,User.create_student
                          ,name="test2", email="test@test.ca", u_email = u_email)
      
    def test_create_event(self):
        """
        Here we are testing the function create event
        """
        name = "mon evenement"
        
        
        
        event_key = self.association.create_event_from(name=name, venue_name =venue_name, description=description, 
                                                  venue_addresse=venue_addresse, date_event=date_event)
        
        event = event_key.get()
        
        self.assertEquals(event.name, name)
        self.assertEquals(event.venue_name, venue_name)
        self.assertEquals(event.venue_addresse, venue_addresse)
        self.assertEquals(event.date_event, date_event)
    
    def test_log_activity(self):
        """
        Here we test the function log Activity
        """
        activity = Activity(category=0)
        self.association.log_activity(activity)
        first_activity = self.association.get_first_ten_activities()[0][0]
        self.assertEqual(activity, first_activity, "the two are not equal")
        
   
    def test_get_ten_activities(self):
        """
        Here we are testing get_ten_activities
        """
        list_of_activities=[]
        for i in range(10):
            activity = Activity(category=0)
            list_of_activities.append(activity)
            self.association.log_activity(activity)
        
        list_of_activities = list(reversed(list_of_activities))
        list_of_ten_activities = self.association.get_first_ten_activities()[0]
        self.assertListEqual(list_of_activities, list_of_ten_activities, "The two lists are equal")
      
    
    def test_is_attending_event(self):
        """
        Testing of the function is_attending_event
        """
        event_key = self.association.create_event_from(name=name, venue_name =venue_name, description=description, 
                                                  venue_addresse=venue_addresse, date_event=date_event)
        event_key2 = self.association.create_event_from(name=name, venue_name =venue_name, description=description, 
                                                  venue_addresse=venue_addresse, date_event=date_event)
        self.association.is_attending_event(event_key)
        
        self.assertTrue(self.association.is_attending_event(event_key))
        
        self.assertFalse(self.association.is_attending_event(event_key2))
       
    
    
def main():
    unittest.main()


if __name__ == '__main__':
    main()