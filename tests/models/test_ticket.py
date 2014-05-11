'''
Created on 6 juin 2013

@author: macbookuser
'''
import unittest

import datetime
from tests.test_utils import OjoTest

from shop.models.ticket import Ticket
from helper_functions import format_datetime

sell_start = datetime.datetime.now()
sell_end = sell_start + datetime.timedelta(5)

ticket_properties=dict({'category':'Private', 'price':500, 'quantity':200, 
                  'section':'A', 'row':'2', 'sell_start':sell_start,
                  'sell_end':sell_end})

ticket_info = dict(ticket_properties)
ticket_info['sell_start'] = format_datetime(ticket_info['sell_start'], format_type="medium")
ticket_info['sell_end'] = format_datetime(ticket_info['sell_end'], format_type="medium")
class TestTicket(OjoTest):
    def setUp(self):
        super(TestTicket, self).setUp()
        ticket = Ticket(**ticket_properties)
        self.ticket = ticket.put()
    
    def test_get_ticket_info_test(self):
        """
        Here we test the function get_ticket_info
        """
        self.assertDictEqual(self.ticket.get().get_ticket_info(), ticket_info)
        
    def test_delete_ticket(self):
        """
        Here we test the function delete ticket
        """
        ticket = self.ticket.get()
        ticket.delete_ticket()
        self.assertIsNone(self.ticket.get())



def main():
    unittest.main()


if __name__ == '__main__':
    main()