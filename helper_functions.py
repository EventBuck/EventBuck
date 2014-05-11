#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 16 mai 2013

@author: Aristote
'''

import webapp2
from google.appengine.ext import ndb
import datetime
import timezone
import re
from conf import UL_DEPARTEMENT

def html5_datetime_parser(unedate):
    """
       Cette fonction est une fonction qui transforme une date entre dans un field form html
       et le transforme en un objet de type datetime.time
       
       :param unedate:
           objet de type string, comprend la date a transformer
           
       :returns:
           objet de type datetime.time
    """
    if not unedate:
        return None
    date, temps = unedate.split("T")
    date = date.split("-")
    temps = temps.split(":")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(temps[0]), int(temps[1]))

def jquery_datepicker_parser(unedate, lang="fr",tzinfo = timezone.Eastern_tzinfo()):
    if not unedate:
        return None
    if unedate.find(" ") < 0:
        
        date = unedate.split("/")
        return datetime.datetime(int(date[2]), int(date[1]), int(date[0]), tzinfo = tzinfo)
    date, temps = unedate.split(" ")
    date = date.split("/")
    temps = temps.split(":")
 
    mydate = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(temps[0]), int(temps[1]), tzinfo=tzinfo)
    return mydate.astimezone(timezone.UTC()).replace(tzinfo=None)
    
def inverse_jquery_datepicker_parser(unedate, tzinfo = timezone.Eastern_tzinfo(), lang="fr"):
    if not unedate:
        return None
    if isinstance(unedate, float):
        unedate = datetime.datetime.fromtimestamp(unedate, tz=tzinfo)
        
    return unedate.strftime("%d/%m/%Y %H:%M",)

def MakeGeoPointFromString(unGeoPt):
    """ Cette fonction permet de transformer une chaine de caractere en un objet
        de type GeoPt que l'on trouve dans le module ndb de Google AppEngine
    """
    if not unGeoPt:
        return None
    longi, lat = unGeoPt.split(',')
    longi = float(longi.strip('('))
    lat = float(lat.strip(')'))
    return ndb.GeoPt(longi, lat)


def get_default_event_image(event_type):
    """ A function that returns the default image for an event 
    """
    if event_type == 'party':
        return '/shop/static/img/party.jpg'
    elif event_type == 'sport':
        return '/shop/static/img/sport.jpg'
    elif event_type == 'academic':
        return '/shop/static/img/academic.jpg'
    else:
        return '/shop/static/img/divers.jpg'
    
def is_email_valid(email):
    valid = re.compile('^[\w.-]+@[\w.-]+')
    return True if valid.match(email) else None
def is_valid_ul_email(email):
    valid = re.compile('^[\w.-]+@ulaval.ca$')
    return True if valid.match(email) else None    

#################################################################################################
#                               
#                                           JINJA FILTERS
#
################################################################################################

def check_active(active, name_of_tab):
    """
       This function allows to check if a tab in the nav is active, if the value of the first param
       is equal to the second param, then the tab is the one that is active
       
       :param active:
           a string that says wich tab must be active
       :param name_of_tab:
           the name of the name of the tab we want to check
       :returns:
           return "active" if name_of_tab is equal to active else empty string
    """
    
    return "active" if active == name_of_tab else ""

def format_from_timestamp(timestamp, format_type="full", tzinfo = timezone.Eastern_tzinfo(), part=None):
    """
    This function take a timestamp, produce a datetime and format it using format_datetime
    """
    date = datetime.datetime.fromtimestamp(timestamp)
    formated_date = format_datetime(date, format_type, tzinfo)
    if part:
        parts = formated_date.split(u" à ")
        
        return parts[0] if part=="date" else parts[1]
    return formated_date

def format_datetime(date, format_type="full", tzinfo = timezone.Eastern_tzinfo()):
    """
    This function is filter used to format datetime object
    """
    months = ['Janvier', u'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre' ]
    days = {'Monday':'Lundi', 'Tuesday':'Mardi', 'Wednesday':'Mercredi', 'Thursday':'Jeudi', 'Friday':'Vendredi', 'Saturday':'Samedi', 'Sunday':'Dimanche'}
    date = date.replace(tzinfo=timezone.UTC()).astimezone(tzinfo)
    
    if format_type == "full":
        
        return u"{0} {1} {2} à {3}".format(days[date.strftime('%A')], date.day, months[(date.month)-1], date.strftime('%H:%M'))
    elif format_type == "medium":
        format_type = "%x A %H:%M"
        return u"{0} {1}/{2}/{3} à {4}".format(days[date.strftime('%A')], date.day, date.month, date.year, date.strftime('%H:%M'))
    
    

def time_elapsed_since_date(date):
    elapsed = datetime.datetime.now() - date
    if elapsed.weeks:
        time_elapsed ="{} weeks ago".format(elapsed.weeks)
    elif elapsed.days:
        time_elapsed = "{} days ago".format(elapsed.days)
    elif elapsed.hours:
        time_elapsed = "{} hours ago".format(elapsed.hours)
    elif elapsed.minutes:
        time_elapsed = "{} minutes ago".format(elapsed.minutes)
    else:
        time_elapsed = " few seconds ago"
        
    return time_elapsed

def get_full_major_name(major_code):
    
    return unicode(UL_DEPARTEMENT.get(major_code, major_code))

def get_category(category):
    category_dict = {'party':'Party', 'other':'Divers', 'academic':u'Académique', 'sport':'Sport'}
    return unicode(category_dict.get(category, category))
def break_to_newline(text):
    """Find every "\n" in text and transform it to "<br\>
    """
    return text.replace('<br>\n','\n')

def is_good_callback(callback, host="http://www.eventbuck.com"):
    """Checks if the passed callback is a valid eventbuck callback
    """
    matchObject = re.match(host, callback)
    return matchObject and matchObject.start() == 0
