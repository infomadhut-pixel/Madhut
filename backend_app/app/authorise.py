from firebase_admin import auth as firebase_auth
from flask import request, jsonify

def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    decoded = firebase_auth.verify_id_token(token)
    return decoded.get("email")