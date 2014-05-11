'''
Created on 4 juin 2013

@author: Aristote Diasonama
'''

from shop.handlers.base_handler import BaseHandler, RpcBaseHandler, user_required
from shop.shop_exceptions import InvalidFormError, UserNotAllowed

class SetPasswordHandler(BaseHandler):

    @user_required
    def post(self):
        try:
            self.validate_form()
            self.change_password()
            self.redirect(self.uri_for('marketMain'))
        except InvalidFormError:
            self.display_message('the password entered didn\'t match')
        except UserNotAllowed :
            self.display_message('The old password is incorrect')
    
    def change_password(self):
        posted_data = self._get_required_data()
        password = posted_data.get('password')
        old_token = posted_data.get('t')
        old_password = posted_data.get('old_password')
        
        if old_password:
            user = self.auth.get_user_by_password(self.user.email, old_password)

            if user['user_id'] != self.user.key.id():

                raise UserNotAllowed('User not allowed to change password')
        
        user = self.user
        user.set_password(password)
        user.put()
        
        # remove signup token, we don't want users to come back with an old link
        if not old_password:
            self.user_model.delete_signup_token(user.get_id(), old_token)
            
            
    def validate_form(self):
        password = self.request.get('confirm_password')
        if not password and password != self.request.get('confirm_password'):
            raise InvalidFormError('The two passwords didn\'t match')
    def _get_required_data(self):
        list_of_data = ['t', 'password', 'confirm_password', 'old_password']
        posted_data = self.cleanPostedData(list_of_data)
        return posted_data

class RpcSetPasswordHandler(RpcBaseHandler, SetPasswordHandler):
    @user_required
    def post(self):
        try:
            self.validate_form()
            self.change_password()
            self.send_success_response()
        except (InvalidFormError, UserNotAllowed) as e:
            self.send_failed_response(error=e)
            
        