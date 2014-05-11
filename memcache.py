#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4 ao�t 2013

@author: Aristote Diasonama
'''
from google.appengine.api import memcache
from market.lib import  sharding_counter

#CLIENT client

CLIENT = memcache.Client() 
def get_mall_key():
    """Return the mall key we are using
    """
    return CLIENT.get('mall_key')

def set_mall_key(mall_key):
    """Save the mall key in the CLIENT
    """
    CLIENT.add('mall_key', mall_key)
    
def get_weekly_sent_ids():
    """
    Get the users who have already been sent a digest for this week
    """
    memcache_key = 'digest-weekly'
    value = CLIENT.get(memcache_key)
    if not value:
        CLIENT.add(memcache_key, [], 86400)
        return []
    else: return value
    
def add_weekly_sent(an_id):
    memcache_key = 'digest-weekly'
    value = CLIENT.get(memcache_key)
    if not value:
        CLIENT.add(memcache_key, [an_id], 86400)
    else:
        value.append(an_id)
        CLIENT.set(memcache_key, value, 86400)

def get_daily_sent_ids():
    """
    """
    memcache_key = 'digest-daily'
    value = CLIENT.get(memcache_key)
    if not value:
        CLIENT.add(memcache_key, [], 86400)
        return []
    else: return value
    
def add_daily_sent(an_id):
    memcache_key = 'digest-daily'
    value = CLIENT.get(memcache_key)
    if not value:
        CLIENT.add(memcache_key, [an_id], 86400)
    else:
        value.append(an_id)
        CLIENT.set(memcache_key, value, 86400)
        
def get_event_attendees_number(event_key, gender=None):
    """
    get the number of attendees of an event given the event_key
    """
    if gender is None:
        return get_event_attendees_number(event_key, 'male') + get_event_attendees_number(event_key, 'female')
    if gender == 'Homme' or gender =='male':
        gender = 'm' 
    else:  gender ='f'
    memcache_key = 'attendees-number-'+gender+'-'+event_key
    return sharding_counter.get_count(memcache_key)
def increment_event_attendees_number(event_key, gender):
    if gender == 'Homme' or gender =='male':
        gender = 'm' 
    else:  gender ='f'
    memcache_key = 'attendees-number-'+gender+'-'+event_key
    return sharding_counter.increment(memcache_key)
def decrement_event_attendees_number(event_key, gender):
    if gender == 'Homme' or gender == 'male':
        gender = 'm' 
    else:  gender ='f'
    memcache_key = 'attendees-number-'+gender+'-'+event_key
    return sharding_counter.decrement(memcache_key)
   
def get_attending_events_keys(user_id):
    """
    Return a list of keys of attending events for user user_id
    return none if no keys is found
    """
    memcache_key = 'attending-event-'+ str(user_id)
    return CLIENT.get(memcache_key)

def set_attending_events_keys(user_id, attending_events):
    """
    save in CLIENT the attending_events dict
    return true if saved else False
    """  
    memcache_key = 'attending-event-'+ str(user_id)
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, attending_events, 1800)
    else:
        return CLIENT.set(memcache_key, attending_events, 1800)  
def update_attending_events_keys(user_id, event_key, attendance_key):
    """
    Update the attending_events dict of this user with a new entry
    """
    
    attending_events_key = get_attending_events_keys(user_id)
    if attending_events_key:
        if not attendance_key:
            del attending_events_key[event_key]
        else:
            attending_events_key[event_key] = attendance_key
                
        set_attending_events_keys(user_id, attending_events_key)
        
def init_following_number(user_id, following_numbers):
    memcache_key = 'following-number-'+ str(user_id)
    return sharding_counter.initCounter(memcache_key, following_numbers)
def get_following_number(user_id):
    memcache_key = 'following-number-' + str(user_id)
    return sharding_counter.get_count(memcache_key)
def increment_following_number(user_id):
    memcache_key = 'following-number-' + str(user_id)
    return sharding_counter.increment(memcache_key)
def decrement_following_number(user_id):
    memcache_key = 'following-number-' + str(user_id)
    return sharding_counter.decrement(memcache_key)
def init_followers_number(user_id, followers_number):
    memcache_key = 'followers-number-'+ str(user_id)
    return sharding_counter.initCounter(memcache_key, followers_number)
def get_followers_number(user_id):
    memcache_key = 'followers-number-' + str(user_id)
    return sharding_counter.get_count(memcache_key)
def increment_followers_number(user_id):
    memcache_key = 'followers-number-' + str(user_id)
    return sharding_counter.increment(memcache_key)

def decrement_followers_number(user_id):
    memcache_key = 'followers-number-' + str(user_id)
    return sharding_counter.decrement(memcache_key)

def get_followers_ids(user_id):
    """Return the list of followers of the user
    """
    memcache_key = 'followers-of-' + str(user_id)
    return CLIENT.get(memcache_key)

def set_followers_ids(user_id, followers_ids):
    memcache_key = 'followers-of-' + str(user_id)
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, followers_ids, 1800)
    else:
        return CLIENT.set(memcache_key, followers_ids, 1800) 

       
def get_following_keys(user_id):
    """Return a dict of (following ids, subscription_key) of the user
    """
    memcache_key = 'following-keys-'+ str(user_id)
    return CLIENT.get(memcache_key)
def set_following_keys(user_id, following_keys):
    """Set the user keys, this user is following
    """
    memcache_key = 'following-keys-'+ str(user_id)
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, following_keys, 1800)
    else:
        return CLIENT.set(memcache_key, following_keys, 1800) 
def get_upcoming_events():
    """
    return upcoming events from CLIENT
    if no events found return None
    """
    return CLIENT.get('up_events')

def set_upcoming_events(up_coming_events):
    """
    save upcoming events in CLIENT, 
    return True if saved else False
    """
    memcache_key = 'up_events'
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, up_coming_events, 86400)
    else:
        return CLIENT.set(memcache_key, up_coming_events, 86400) 

def delete_event(event_key):
    """
    Delete the event from upcoming_events
    """
    upcoming_events = get_upcoming_events()
    if upcoming_events and upcoming_events.get(event_key):
        del upcoming_events[event_key]
        set_upcoming_events(upcoming_events)
def get_recent_events():
    """
    return upcoming events from CLIENT
    if no events found return None
    """
    return CLIENT.get('recent_events')

def set_recent_events(recent_events):
    """
    save upcoming events in CLIENT, 
    return True if saved else False
    """
    memcache_key = 'recent_events'
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, recent_events, 86400)
    else:
        return CLIENT.set(memcache_key, recent_events, 86400) 

def delete_up_coming_events():
    """
    delete upcoming events from CLIENT
    """
    CLIENT.delete('recent_events')
    return CLIENT.delete('up_events')

def get_users():
    """
    return users dict from CLIENT
    if no users found return None
    """
    return CLIENT.get('users')

def set_users(user_list):
    """
    save users dict in CLIENT, 
    return True if saved else False
    """
    memcache_key = 'users'
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, user_list, 86400)
    else:
        return CLIENT.set(memcache_key, user_list, 86400) 

def delete_user_list():
    """
    delete users dict from CLIENT
    """
    return CLIENT.delete('users')


def get_user(user_id):
    return CLIENT.get(str(user_id))

def set_user(user_id, user):
    memcache_key = str(user_id)
    if not CLIENT.get(memcache_key):
        return CLIENT.add(memcache_key, user, 86400)
    else:
        return CLIENT.set(memcache_key, user, 86400)

def init_total_users(number):
    memcache_key = 'total-users'
    sharding_counter.initCounter(memcache_key, number)

def increment_total_users():
    memcache_key = 'total-users'
    return sharding_counter.increment(memcache_key)
def decrement_total_users():
    memcache_key = 'total-users'
    return sharding_counter.decrement(memcache_key)
def get_total_users():
    memcache_key = 'total-users'
    return sharding_counter.get_count(memcache_key)

def get_update_lock():
    memcache_key = 'update-lock'
    return CLIENT.get(memcache_key)
def put_update_lock():
    memcache_key = 'update-lock'
    return CLIENT.add(memcache_key, 1)
def remove_update_lock():
    memcache_key = 'update-lock'
    return CLIENT.delete(memcache_key)