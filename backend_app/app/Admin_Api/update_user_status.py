from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.user_data import UserDatabase
from flask import request

blp = Blueprint("admin update user status", __name__)


@blp.route('/admin/update/user/status')
class UpdateStatus(MethodView):
    def __init__(self):
        self.user_db = UserDatabase()

    def put(self):
        data = request.get_json()
        user_id = data["user_id"]
        status = data['status']
        response = self.user_db.update_user_status(
            user_id, status
        )
        return response
