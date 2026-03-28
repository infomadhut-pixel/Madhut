from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.User.user_data import UserDatabase
from ..authorise import get_current_user

blp = Blueprint('user profile', __name__)


@blp.route("/user/profile")
class UserProfile(MethodView):
    def __init__(self):
        self.user_db = UserDatabase()

    def get(self):
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401
        result = self.user_db.find_user(email)
        return result
