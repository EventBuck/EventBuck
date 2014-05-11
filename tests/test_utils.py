'''
Created on 6 juin 2013

@author: Aristote Diasonama
'''
import unittest


from google.appengine.ext import testbed

class OjoTest(unittest.TestCase):
    def runTest(self):
        pass
    
    def setUp(self):
    # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
    # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()