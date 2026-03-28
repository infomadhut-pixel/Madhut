from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.T_shirt.tshirt_reviews import Review
from flask import request

blp = Blueprint("admin delete unfair or spam review", __name__)


@blp.route("/admin/delete/unfair/review")
class AdminDeleteReview(MethodView):
    def __init__(self):
        self.review_db = Review()

    def delete(self):
        _id = request.args.get("id")
        print(_id)
        response = self.review_db.delete_review(_id)
        return response
