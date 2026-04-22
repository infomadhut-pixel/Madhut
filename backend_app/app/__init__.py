from flask import Flask, jsonify
from flask_cors import CORS
from .User_Api import register_user_blueprint
from .Admin_Api import register_admin_blueprint
from .config import configure_app
from .extensions import api, jwt, mail
from .Database.User.user_data import UserDatabase
from .Database.User.check_out import OrderTshirt
from app.extensions import bcrypt
from .User_Api.Blocklist import Blocklist
import os
import json
import firebase_admin
from firebase_admin import credentials
from .extensions import cache
from flask_compress import Compress


# from .extensions import limiter


def create_app():
    app = Flask(__name__)
    bcrypt.init_app(app)
    configure_app(app)
    Compress(app)
    # limiter.init_app(app)

    user_db = UserDatabase()
    user_db.create_index()
    order_db = OrderTshirt()
    order_db.create_order_index()
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

    @app.route("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200

    if not firebase_credentials:
        raise ValueError("FIREBASE_CREDENTIALS not set in environment")

    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "https://madhut-kp2y.vercel.app",
                    "http://localhost:63342",
                    "https://madhut-itey-g4e8o3ga8-harshkumartiwari034s-projects.vercel.app",
                    "https://madhut-wine.vercel.app"
                ]
            }
        },
        supports_credentials=False
    )
    api.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return Blocklist.contains(jwt_payload["jti"])

    register_user_blueprint(api)
    register_admin_blueprint(api)

    return app
