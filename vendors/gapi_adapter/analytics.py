#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 1 janv. 2014

@author: didia
'''

import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from admin.secure import GA_PROFILE_ID
CLIENT_SECRETS = 'client_secrets.json'
# A helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

# A file to store the access token
TOKEN_FILE_NAME = 'analytics.dat'

def prepare_credentials():
    # Retrieve existing credendials
    storage = Storage(TOKEN_FILE_NAME)
    credentials = storage.get()

    # If existing credentials are invalid and Run Auth flow
    # the run method will store any new credentials
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage) #run Auth Flow and store credentials

    return credentials

def initialize_service():
  
    http = httplib2.Http()

    credentials = prepare_credentials()
    http = credentials.authorize(http)  # authorize the http object


    return build('analytics', 'v3', http=http)


def get_page_view(date,url):
    try:
        service = initialize_service()
        return service.data().ga().get(
      ids=GA_PROFILE_ID,
      start_date='2012-01-01',
      end_date='2012-01-15',
      metrics='ga:visits',
      dimensions='ga:source,ga:keyword',
      sort='-ga:visits',
      filters='ga:medium==organic',
      start_index='1',
      max_results='25')
    except TypeError, error:
        # Handle errors in constructing a query.
        print ('There was an error in constructing your query : %s' % error)

    except HttpError, error:
        # Handle API errors.
        print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')
