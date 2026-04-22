from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.user_data import UserDatabase
from flask import request

blp = Blueprint("admin seen all user", __name__)


@blp.route('/get/all/user')
class AllUser(MethodView):
    def __init__(self) -> None:
        self.user_db = UserDatabase()

    def post(self):
        data = request.get_json()
        page = int(data.get("page", 1))
        limit = int(data.get("limit", 10))
        skip = (page - 1) * limit
        user, total = self.user_db.get_all_user(skip, limit)
        return {
            "data": user,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1)
        }, 200
