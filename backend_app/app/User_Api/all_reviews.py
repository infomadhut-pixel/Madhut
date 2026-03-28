from flask.views import MethodView
from flask_smorest import Blueprint
from ..authorise import get_current_user
from ..Database.T_shirt.tshirt_reviews import Review
from flask import request

blp = Blueprint("user seen all review", __name__)


@blp.route('/get/all/reviews')
class GetAllReview(MethodView):
    def __init__(self):
        self.review_db = Review()

    def post(self):
        get_current_user()
        product_id = request.args.get('product_id')
        response = self.review_db.get_reviews(product_id)
        return response
