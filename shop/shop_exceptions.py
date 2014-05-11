#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 31 mai 2013

@author: macbookuser
'''
import webapp2

class ShopException(Exception):
    """
    Base class for all shop exceptions
    """
    pass
    

class RpcShopException(ShopException, webapp2.HTTPException):
    """
        This Exception is raised when an rpc activity didn't complete well
    """
    def __init__(self, message='Something went bad', code=500):
        
        self.code = code
        ShopException.__init__(self, message)

class UserAlreadyExistError(RpcShopException):
    """
    This exception is raised when the we are unable to create a user
    the code for this error is 409
    """
    def __init__(self, message="Unable to create user"):
        
        super(UserAlreadyExistError, self).__init__(message=message, code=409) 

class UserNotFoundError(RpcShopException):
    """
    This exception is raised when the user we are searching for doesn't exist anymore
    the code for this error is 404
    """
    def __init__(self, message="Unable to find user"):
        
        super(UserNotFoundError, self).__init__(message=message, code=404)
         
class UserNotAllowed(RpcShopException):
    """This exception is raised when a user try to do an action not allowed
    """
    def __init__(self, message="User not allowed to take action"):
        
        super(UserNotAllowed, self).__init__(message, code=403)
        
class EventNotFoundException(RpcShopException):
    """
    This Exception is raised when the user is looking for an event that doesn't exist in the database
    """
    def __init__(self, message = "The event was not found"):

        super(EventNotFoundException, self).__init__(message=message, code=404)
        
        
class TicketNotFoundException(RpcShopException):
    """
    This Exception is raised when the user is looking for an event that doesn't exist 
    """
    def __init__(self, message = "The Ticket was not found"):
        
        super(TicketNotFoundException, self).__init__(message=message, code=404)
    
    
    
   


        
class InvalidFormError(RpcShopException):
    """
    This exception is raised when form validation function fails
    the code for this error is 400
    """
    def __init__(self, message="Invalid form submitted"):
        super(InvalidFormError, self).__init__(message=message, code=400)

class NoActivitiesFoundError(ShopException):
    """
    This exceptions is raised when we are looking up for a user's activities
    and user doesn't have any
    """
    pass
class LogActivityError(ShopException):
    """
    This exception is raised when None or an Object not of type Activity
    is passed to log_activity function
    """
    pass
class BadArgumentForActivityError(ShopException):
    """
    This exception is raised when a bad number type is provided when creating
    an activity
    """
    pass
class TicketCreationFailedError(ShopException):
    """
    This exception is raised when we fail to create a ticket
    """
    pass
class TicketEditionFailedError(ShopException):
    """
    This exception is raised the edition of a ticket fails
    """
    pass
class InvalidEventError(ShopException):
    """
    This error is raised when the event being published is not valid
    """
    pass

class EventInMarketError(ShopException):
    """
    This error is raised when trying to delete an event currently in market
    """
    pass