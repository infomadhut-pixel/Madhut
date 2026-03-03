from flask import Flask
from flask_cors import CORS
from .User_Api import register_user_blueprint
from .Admin_Api import register_admin_blueprint
from .config import configure_app
from .extensions import api, jwt, mail
from .Database.User.user_data import UserDatabase
from app.extensions import bcrypt
from .User_Api.Blocklist import Blocklist


def create_app():
    app = Flask(__name__)
    bcrypt.init_app(app)
    configure_app(app)

    user_db = UserDatabase()
    user_db.create_index()
    import firebase_admin
    from firebase_admin import credentials

    cred = credentials.Certificate("D:/MadHut/backend_app/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:63342"
                ]
            }
        },
        supports_credentials=False
    )

    api.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return Blocklist.contains(jwt_payload["jti"])

    register_user_blueprint(api)
    register_admin_blueprint(api)

    return app
