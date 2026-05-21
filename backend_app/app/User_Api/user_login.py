from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from firebase_admin import auth as firebase_auth
from ..Database.User.user_data import UserDatabase
import logging

logger = logging.getLogger(__name__)

blp = Blueprint('user login', __name__, description='firebase login')


@blp.route('/user/login')
class UserLogin(MethodView):
    def __init__(self):
        self.user_db = UserDatabase()

    # @limiter.limit("2 per minute")
    def post(self):

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"message": "Invalid token format"}, 401

        token = auth_header.split(" ")[1]

        decoded_token = firebase_auth.verify_id_token(token)

        email = decoded_token.get("email")
        logger.info(f"Firebase verified for {email}")
        uid = decoded_token.get("uid")
        logger.info(f"Existing user login: {email}")

        user = self.user_db.find_user(email)
        if user:
            if user.get("is_active") is False:
                logger.warning(f"Blocked user tried login: {email}")
                return {
                    "message": "Your account is deactivated.",
                    "status": False,
                    "blocked": True
                }, 200
        else:
            data = request.get_json()
            self.user_db.register_user(
                data.get("username"),
                email,
                data.get("phone"),
                data.get("street"),
                data.get("pin_code"),
                data.get("country")
            )

        return {
            "message": "Login successful",
            "email": email,
            "uid": uid
        }
