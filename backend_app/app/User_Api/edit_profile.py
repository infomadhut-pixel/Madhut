from flask_smorest import Blueprint
from flask.views import MethodView
from ..authorise import get_current_user
from ..Database.User.user_data import UserDatabase
from flask import request

blp = Blueprint('edit profile', __name__)


@blp.route('/user/edit/profile')
class UserEditProfile(MethodView):
    def __init__(self):
        self.edit_profile = UserDatabase()

    def patch(self):
        data = request.get_json()
        email = get_current_user()
        updated_data = {}
        if 'contact_number' in data:
            updated_data["contact_number"] = data['contact_number']
        if 'street' in data:
            updated_data["street"] = data['street']
        if 'pin_code' in data:
            updated_data["pin_code"] = data['pin_code']
        if 'country' in data:
            updated_data["country"] = data['country']

        response = self.edit_profile.update_profile(email, updated_data)
        return response
