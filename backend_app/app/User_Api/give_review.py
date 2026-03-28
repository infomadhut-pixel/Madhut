from flask.views import MethodView
from flask_smorest import Blueprint
from ..authorise import get_current_user
from ..Database.T_shirt.tshirt_reviews import Review
from ..Database.User.check_out import OrderTshirt
from flask import request

blp = Blueprint('user give reviews for tshirt', __name__)


@blp.route('/user/give/reviews')
class AddReviews(MethodView):
    def __init__(self):
        self.review_db = Review()
        self.order_db = OrderTshirt()

    def post(self):
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401

        data = request.get_json()
        product_id = data["product_id"]
        order_id = data['order_id']
        name = data['user_name']
        rating = data['rating']
        feedback = data['comment']
        response = self.review_db.add_reviews(product_id, name, rating, feedback)
        self.order_db.update_review_status(order_id)
        return response
