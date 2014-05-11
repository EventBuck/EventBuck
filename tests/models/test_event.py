'''
Created on 6 juin 2013

@author: macbookuser
'''
import unittest
import datetime


from tests.test_utils import OjoTest
from shop.models.event import Event

from shop.shop_exceptions import InvalidEventError
from shop.shop_exceptions import EventInMarketError



event_name ="PaidEvent 1" 
event_date = datetime.datetime.now() + datetime.timedelta(hours = 8)
venue_name = "Venue 1"
venue_addresse = "addresse 1"
ticket_info = {'price':20, 'quantity':30, 'sell_start':datetime.datetime.now(), 'sell_end': datetime.datetime.now()+datetime.timedelta(hours=4)}

class PaidEventTest(OjoTest):
    def setUp(self):
        super(PaidEventTest, self).setUp()
        self.event = Event(type = 'paid', name = event_name, date_event=event_date, venue_name = venue_name, venue_addresse = venue_addresse, description = "event 1")
        self.valid_event = Event(type = 'paid', name = event_name, date_event=event_date, venue_name = venue_name, venue_addresse = venue_addresse, description = "event 1")
        self.valid_event.put()
        self.valid_event.create_ticket_from(**ticket_info)
        key = self.event.put()
        self.event = key
    def get_valid_event_key(self):
        event = self.event.get()
        event.create_ticket_from(**ticket_info)
        return event.put()
       
class TestValidatePaidEvent(PaidEventTest):
    """
    This class test the function validate_event
    validate_event returns True when an event is valid and false when not
    An event is valid when the date_event is not already passed or when the event has tickets
    """
    def test_valid_case_event_is_valid(self):
        """
        When an event has tickets and date_event is not passed.
        """
        event = self.valid_event
    
        self.assertTrue(event.validate_event())
    def test_invalid_case_event_has_no_tickets(self):
        """
        Test cases when ticket doesn't have tickets
        """
        event = self.event.get()
        self.assertIs(event.validate_event(), False)
    
    def test_invalid_case_date_event_passed(self):
        """
        Test cases when date_event is passed. Here we set the date to point 
        4 hours behind ago
        """
       
        event = self.event.get()
        
        event.date_event = datetime.datetime.now() + datetime.timedelta(hours = -40)
        self.assertIs(event.validate_event(), False)
    

    
class TestPublishPaidEvent(PaidEventTest):
    """
    This class test the function publish_event.
    publish an event if the event is valid and
    raises InvalidPaidEventError if it's not valid 
    """
    def test_valid_case_event_is_valid(self):
        """
        Test a valid case when the event is valid. This must not raise an exception
        """
        event = self.valid_event
        
        try:
            event.publish_event()
            
            self.assertTrue(event.published)
        except InvalidEventError:
            self.fail("Raised InvalidPaidEventError while the event was valid")
    
    def test_invalid_case_event_is_not_valid(self):
        """
        Test an invalid case when the event is not valid. This must raise an exception
        """
        event = self.event.get()
        
        self.assertRaises(InvalidEventError, Event.publish_event, event)

class TestDeletePaidEvent(PaidEventTest):
    """
    This class test the function delete_event.
    delete_event delete an event from the database if the event has not yet been published.
    or if it has been published and date_event not passed it raises PaidEventInMarketError
    and in case the event has already taken place, it sets the deleted flag true
    """
    def test_valid_case_event_not_published(self):
        """
        delete an event that has not yet been published.
        When trying to get the event None is returned
        """
        key = self.event
        event = self.event.get()
        event.delete_event()
        
        self.assertIsNone(key.get()) 

    def test_valid_case_event_taken_place(self):
        """
        delete an event that has already taken place
        Set the event.deleted flag to true
        """
        event = self.valid_event
        event.publish_event()
        event.date_event = datetime.datetime.now() + datetime.timedelta(hours = -4)
        event.delete_event()
        self.assertTrue(event.deleted, "when an event that has taken place is deleted, his deleted flag must be true")
            
class TestCancelPaidEvent(PaidEventTest):
    """
    This class is used to test the function cancel_event. 
    This function is set to  cancel an event.
    """ 
    pass

class TestDeleteTicket(PaidEventTest):
    """
    This class is used to test the function delete ticket of an event.
    This class deletes ticket is the event is not published. If the event is
    published it raises PaidEventInMarketError
    """
    def test_valid_case_event_not_published(self):
        """
        test delete_ticket with a not yet published event. 
        the ticket must be deleted from the database
        """
        event = self.valid_event
        ticket_key = event.create_ticket_from(**ticket_info)
        
        event.delete_ticket(ticket_key.id())
        
        self.assertIsNone(ticket_key.get())
    
    def test_invalid_case_event_published(self):
        """
        test delete_ticket with a published event
        Must raise PaidEventInMarketError
        """
        event = self.valid_event
        ticket_key = event.create_ticket_from(**ticket_info)
        event.publish_event()
        self.assertRaises(EventInMarketError, Event.delete_ticket, event, ticket_key.id())
    
        
def main():
    unittest.main()


if __name__ == '__main__':
    main()
    