#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Created on 1 juil. 2013

@author: Aristote Diasonama

Router for the app
'''

import webapp2
from webapp2_extras import routes

from market.handlers.template_viewer import TemplateViewer, ChannelViewer
from market.handlers.main import MainHandler, RpcMainGetEvents
from market.handlers.crons import UpdateMall

from market.handlers.contacting.contacting import RpcContactingHandler

from market.handlers.community.show import ShowCommunityHandler, RpcShowCommunityHandler
from market.handlers.community.facebook_invite import FacebookInviteHandler

from market.handlers.event.image import ImageHandler
from market.handlers.event.attending import RpcAttendEvent, ShowAttendingHandler, RpcAttendingGetEvents
from market.handlers.event.user_events import ShowEventHandler as MarketShowEvent
from market.handlers.event.user_events import CreateEventHandler as MarketCreateEvent
from market.handlers.event.user_events import EditEventHandler as MarketEditEvent
from market.handlers.event.view import ViewEventHandler
from market.handlers.event.reporting import RpcReportingHandler

from market.handlers.mall.get import RpcGetHandler

from market.handlers.notification.daily_notification import StartDailyNotificationHandler
from market.handlers.notification.daily_notification import CreateDailyNotificationHandler
from market.handlers.notification.daily_notification import SendDailyNotificationHandler
from market.handlers.notification.weekly_notification import StartWeeklyNotificationHandler
from market.handlers.notification.weekly_notification import CreateWeeklyNotificationHandler
from market.handlers.notification.weekly_notification import SendWeeklyNotificationHandler

from market.handlers.profile.login_logout import LoginHandler, LogoutHandler, Authenticate
from market.handlers.profile.signup import SignupHandler, FacebookSignup, RpcSignupHandler, RpcFacebookSignup
from market.handlers.profile.verification import VerificationHandler, RpcResendVerificationLink
from market.handlers.profile.forgot_password import RpcForgotPasswordHandler
from market.handlers.profile.set_password import RpcSetPasswordHandler
from market.handlers.profile.view import ViewProfileHandler
from market.handlers.profile.subscription import RpcSubscribe, ShowFollowers, ShowFollowing, ShowEventsFromSubscription,RpcSubscriptionGetEvents
from market.handlers.profile.edit import RpcEditUser as MarketRpcEditUser, EditUserHandler, RpcEditNotification
from market.handlers.event.publish_delete_cancel import RpcPublishEventHandler, RpcDeleteEventHandler


from shop.handlers.main_handler import MainHandler as ShopMainHandler, RpcLoadMoreActivities

from shop.handlers.profile.login_logout_handler import LoginHandler as ShopLoginHandler, LogoutHandler as ShopLogoutHandler
from shop.handlers.profile.signup_handler import SignupHandler as ShopSignupHandler
from shop.handlers.profile.verification_handler import VerificationHandler as ShopVerificationHandler
from shop.handlers.profile.profile_image_handler import ProfileImageHandler as ShopProfileImageHandler


from shop.handlers.event.create import CreateEventHandler, RpcCreateEventHandler
from shop.handlers.event.edit import EditEventHandler, RpcCreateEventImage, RpcEditEventHandler
from shop.handlers.event.show import ShowEventHandler
from shop.handlers.event.image import ImageHandler as ShopImageHandler

from shop.handlers.ticket.create_ticket_handler import CreateTicketHandler
from shop.handlers.ticket.create_ticket_handler import RpcCreateTicketHandler
from shop.handlers.ticket.edit_ticket_handler import EditTicketHandler
from shop.handlers.ticket.edit_ticket_handler import RpcEditTicketHandler
from shop.handlers.ticket.show_ticket_handler import ShowTicketHandler

from admin.handlers.dev_server_tasks import UpdateEvent, PopulateEvent, CreateShop , VerifyUser

from admin.handlers.reports import ShowReportHandler
from admin.handlers.mainAdmin import MainAdminHandler

from shop.handlers.template_viewer import TemplateViewer as ShopTemplateViewer



__all__ = ['applications_routes']

applications_routes = []


_main_routes = [routes.PathPrefixRoute('/rpc', [
                                   webapp2.Route('/signup', RpcSignupHandler, name="rpcMarketSignUp"),
                                   webapp2.Route('/signup/fb', RpcFacebookSignup),
                                   webapp2.Route('/forgot', RpcForgotPasswordHandler, name="rpcForgot"),
                                   webapp2.Route('/reset_password', RpcSetPasswordHandler, name="rpcResetPassword"),             
                                   webapp2.Route('/contact', RpcContactingHandler, name="contacting" ),
                                   webapp2.Route('/mall/events', RpcGetHandler, name="getEvents" ),
                                   webapp2.Route('/event/attend', RpcAttendEvent, name="attendEvent"),
                                   webapp2.Route('/event/report', RpcReportingHandler, name="reportEvent"),
                                   webapp2.Route('/edit', MarketRpcEditUser, name="rpcEditUser"),
                                   webapp2.Route('/edit/notifications', RpcEditNotification),
                                   webapp2.Route('/<user_id:[\d]+>/subscribe', RpcSubscribe, name = "subscribe"),
                                   webapp2.Route('/attending', RpcAttendingGetEvents),
                                   webapp2.Route('/community/<page>', RpcShowCommunityHandler),
                                   webapp2.Route('/community', RpcShowCommunityHandler),
                                   webapp2.Route('/subscription', RpcSubscriptionGetEvents),
                                   webapp2.Route('/verification', RpcResendVerificationLink),
                                   
                                   webapp2.Route('/<page>', RpcMainGetEvents),
                                   webapp2.Route('/', RpcMainGetEvents),  
                                   routes.PathPrefixRoute('/myevents', [
                                  
                                       webapp2.Route('/create', RpcCreateEventHandler, name="rpcCreateEvent" ),
                                       webapp2.Route('/edit/<event_id:[\d]+>', RpcEditEventHandler, name="rpcEditEvent"),
                                       webapp2.Route('/edit/<event_id:[\d]+>/picture', RpcCreateEventImage, name="rpcEditEventPicture"),
                                       
                                       webapp2.Route('/', MarketShowEvent)
                                                              ]),                        
                                   ]),
                routes.PathPrefixRoute('/crons', [
                                                  
                                 webapp2.Route('/notification/daily', StartDailyNotificationHandler),
                                 webapp2.Route('/notification/weekly', StartWeeklyNotificationHandler)                                 
                                                     
                                                     ]),
                routes.PathPrefixRoute('/tasks', [
                                 webapp2.Route('/notification/daily/start', CreateDailyNotificationHandler),                  
                                 webapp2.Route('/notification/daily', SendDailyNotificationHandler), 
                                 webapp2.Route('/notification/weekly/start', CreateWeeklyNotificationHandler),                  
                                 webapp2.Route('/notification/weekly', SendWeeklyNotificationHandler),                                 
                                                    
                                                     ]),
                routes.PathPrefixRoute('/myevents', [
                                  
                                   webapp2.Route('/create', MarketCreateEvent, name="marketCreateEvent" ),
                                   webapp2.Route('/edit/<event_id:[\d]+>', MarketEditEvent, name="marketEditEvent"),
                                   webapp2.Route('/', MarketShowEvent)
                                                              ]),
                routes.PathPrefixRoute('/admin', [
                                
                                   routes.PathPrefixRoute('/update',[
                                        webapp2.Route('/event', UpdateEvent),
                                        webapp2.Route('/shop', CreateShop)
                                                              
                                                                   ]),
                                    routes.PathPrefixRoute('/populate',[
                                        webapp2.Route('/event', PopulateEvent)
                                                              
                                                                   ]),
                                   webapp2.Route('/template/<template:[\w]+>', TemplateViewer),
                                   webapp2.Route('/market/tasks/update', UpdateMall),
                                   webapp2.Route('/verify/user', VerifyUser),
                                   webapp2.Route('/reports',ShowReportHandler, name="adminShowReports" )
                                   
                                                              ]),
                routes.PathPrefixRoute('/<user_id:[\d]+>', [
                                  
                                   webapp2.Route('/followers', ShowFollowers, name = "viewFollowers"),
                                   webapp2.Route('/following', ShowFollowing, name="viewFollowing"),
                                   webapp2.Route('/<event_id:[\d]+>', ViewEventHandler, name="viewEvent"),
                                   webapp2.Route('/image', ShopProfileImageHandler, name="userProfileImage"),
                                    ]),
                               webapp2.Route('/rpc', RpcMainGetEvents),
                               webapp2.Route('/<user_id:[\d]+>', ViewProfileHandler, name="viewUser"),
                               webapp2.Route('/edit/<section>', EditUserHandler),
                               webapp2.Route('/edit', EditUserHandler, name="editUser"),
                               webapp2.Route('/signin', LoginHandler, name="marketLogin"),
                               webapp2.Route('/authenticate', LoginHandler, methods=['POST']),
                               webapp2.Route('/authenticate', Authenticate, methods=['GET'], name="marketAuthenticate"),
                               
                               webapp2.Route('/signup', SignupHandler, name="marketSignUp"),
                               webapp2.Route('/signup/fb', FacebookSignup, name="marketSignUpFb"),
                               webapp2.Route('/logout', LogoutHandler, name="marketLogout"),
                               webapp2.Route('/verification', VerificationHandler, name="marketVerification"),
                               webapp2.Route('/myevents', MarketShowEvent, name="marketUserEvents"),
                               webapp2.Route('/subscription', ShowEventsFromSubscription, name="marketSubscription"),
                               webapp2.Route('/attending', ShowAttendingHandler, name="marketUserAttending"),
                               
                               
                               webapp2.Route('/event/image/<event_key>', ImageHandler, name="marketImageEvent"),
                               webapp2.Route('/admin', MainAdminHandler ),
                               webapp2.Route('/_ah/warmup', UpdateMall),
                               webapp2.Route('/shop', ShopMainHandler),
                               webapp2.Route('/community/facebook_invite/', FacebookInviteHandler),
                               webapp2.Route('/community/facebook_invite', FacebookInviteHandler),
                               webapp2.Route('/community/<page>', ShowCommunityHandler),
                               webapp2.Route('/community', ShowCommunityHandler),
                               webapp2.Route('/channel/', ChannelViewer),
                               webapp2.Route('/<page>', MainHandler, name = 'market' ),
                               
                               webapp2.Route('/', MainHandler, name = 'marketMain' )]

for route in _main_routes:
    applications_routes.append(route)
    



_shop_routes = [routes.PathPrefixRoute('/shop', [
                                    routes.PathPrefixRoute('/rpc',[
                                        webapp2.Route('/createTicket/<event_id:[\d]+>', RpcCreateTicketHandler, name="rpc_createTicket"),
                                        webapp2.Route('/editTicket/<event_id:[\d]+>/<ticket_id:[\d]+>', RpcEditTicketHandler, name="rpc_editTicket"),
                                        webapp2.Route('/loadActivities', RpcLoadMoreActivities, name="rpc_load_more"),  
                                        webapp2.Route('/publishEvent/<event_id:[\d]+>', RpcPublishEventHandler, name="rpc_publishEvent"),
                                        webapp2.Route('/deleteEvent/<event_id:[\d]+>',RpcDeleteEventHandler, name="rpc_deleteEvent")                       
                                                                   ]),
                                                                
                                    
                                                                
                                    webapp2.Route('', ShopMainHandler),                           
                                    webapp2.Route('/', ShopMainHandler),
                                    webapp2.Route('/signup', ShopSignupHandler, name="shopSignUp"),
                                    webapp2.Route('/signin', ShopLoginHandler, name="shopLogin"),
                                    webapp2.Route('/logout', ShopLogoutHandler, name="shopLogout"),
                                    webapp2.Route('/verification', ShopVerificationHandler, name="shopVerification"),
                                    webapp2.Route('/profile/picture', ShopProfileImageHandler, name="profilePicture"),
                                    webapp2.Route('/createEvent', CreateEventHandler, name="createEvent"),
                                    webapp2.Route('/showEvent', ShowEventHandler, name="showEvent"),
                                    webapp2.Route('/editEvent/<event_id:[\d]+>', EditEventHandler, name="editEvent"),
                                    webapp2.Route('/event/image/<event_id:[\d]+>', ShopImageHandler, name="imageEvent"),
                                    
                                    webapp2.Route('/createTicket/<event_id:[\d]+>', CreateTicketHandler, name="createTicket"),
                                    webapp2.Route('/showTicket/<event_id:[\d]+>', ShowTicketHandler, name="showTicket"),
                                    webapp2.Route('/editTicket/<event_id:[\d]+>/<ticket_id:[\d]+>', EditTicketHandler, name="editTicket"),
                                    
                                    webapp2.Route('/template/<template:[\w]+>', ShopTemplateViewer),
                                    ]),
                webapp2.Route('/shop', ShopMainHandler, name="shopMain")]

for route in _shop_routes:
    applications_routes.append(route)                        
                                    
