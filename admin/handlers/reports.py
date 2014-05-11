#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 30 ao�t 2013

@author: Aristote Diasonama
'''

from market.handlers.base import BaseHandler
from shop.handlers.base_handler import user_required
from shop.models.report import Report

class ShowReportHandler(BaseHandler):
    @user_required
    def get(self):  
        context = self.get_template_context()
        self.render_template('admin_reports.html', context)
    def get_template_context(self):
        context = {}
        reports = Report.get_all()
        reports_and_events = []
        for a_report in reports:
            report = dict(a_report.get_report_in_dict())
            
            reporter = self._get_user_by_key(report['reported_by'])
            if reporter.type == 'student':
                report['reporter'] = " ".join((reporter.firstname, reporter.name))
            else:
                report['reporter'] = reporter.name
            report['reporter_id'] = reporter.key.id()
            report['reporter_type'] = reporter.type
            report['event'] = self.get_event_with_context(a_report.event.get().get_event_in_dict())
            
            reports_and_events.append(report)
        context['reports'] = reports_and_events
        context['left_sidebar'] = 'reports'
        return context
   
        
