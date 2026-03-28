from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.T_shirt.tshirt_reviews import Review

blp = Blueprint("seen and verify review", __name__)


@blp.route('/admin/seen/verify/review')
class VerifyReview(MethodView):
    def __init__(self):
        self.review_db = Review()

    def post(self):
        response = self.review_db.get_all_reviews()
        return response
