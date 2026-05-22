from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from firebase_admin import auth as firebase_auth
from ..Database.User.user_data import UserDatabase
from ..Database.User_Log_Details.user_logs import SaveUserActivity
import logging
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

blp = Blueprint('user login', __name__, description='firebase login')


@blp.route('/user/login')
class UserLogin(MethodView):
    def __init__(self):
        self.user_db = UserDatabase()
        self.user_activity = SaveUserActivity()

    # @limiter.limit("2 per minute")
    def post(self):

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"message": "Invalid token format"}, 401

        token = auth_header.split(" ")[1]

        decoded_token = firebase_auth.verify_id_token(token)

        email = decoded_token.get("email")
        logger.info(f"Firebase verified for {email}")
        ip_address = request.headers.get(
            "X-Forwarded-For",
            request.remote_addr
        ).split(",")[0]
        location = {}
        if ip_address != "127.0.0.1":
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            location = response.json()
        user_agent = request.user_agent.string

        login_time = datetime.utcnow()
        uid = decoded_token.get("uid")
        activity_data = {
            "email": email,
            "uid": uid,
            "ip_address": ip_address,
            "country": location.get("country"),
            "city": location.get("city"),
            "region": location.get("region"),
            "regionName": location.get("regionName"),
            "postal_code": location.get("zip"),
            "latitude":location.get("lat"),
            "longitude":location.get("lon"),
            "device": user_agent,
            "login_time": login_time,
            "action": "login"
        }
        self.user_activity.save_user_activity(activity_data)

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
