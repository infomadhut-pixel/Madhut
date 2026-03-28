from firebase_admin import auth as firebase_auth
from flask import request

def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        decoded = firebase_auth.verify_id_token(token, clock_skew_seconds=10)
        return decoded.get("email")

    except Exception:
        return None