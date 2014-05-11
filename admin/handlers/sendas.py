#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 3 sept. 2013

@author: Aristote Diasonama
'''

import gdata.apps.emailsettings.client
from admin import secure

client = gdata.apps.emailsettings.client.EmailSettingsClient(domain='eventbuck.com')
client.ClientLogin(email=secure.GOOGLE_ACCOUNT, password=secure.GOOGLE_PASSWORD, source='ojo-ticket')
print(client.CreateSendAs(username=secure.GOOGLE_USERNAME, name='Support', address='support@eventbuck.com'))