#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 25 juil. 2013
@author: Aristote Diasonama
'''
import webapp2

class MarketException(Exception):
    """
    Base Class for all market exceptions
    """
    pass

class RpcMarketException(MarketException, webapp2.HTTPException):
    """
    Base Class for Client Rpc Request Exception
    """
    def __init__(self, message='Something went bad', code=500):
        
        self.code = code
        MarketException.__init__(self, message)

class UserNotFoundError(MarketException):
    """
    This exception is raised when we are unable to find a given user in the database
    """
    pass
class NoEventsFoundException(MarketException):
    """
    This exception is raised when there is no events available in the market
    """
    pass