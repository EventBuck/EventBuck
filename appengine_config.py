#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 27 juil. 2013

@author: Aristote Diasonama
'''
appstats_CALC_RPC_COSTS = True

def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app