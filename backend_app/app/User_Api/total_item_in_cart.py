from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.User.add_to_cart import AddToCart
from ..authorise import get_current_user

blp = Blueprint('fetch number of items add in cart', __name__)


@blp.route('/fetch/total/item/in/cart')
class TotalItemCart(MethodView):
    def __init__(self):
        self.cart_db = AddToCart()

    def get(self):
        try:
            email = get_current_user()
            if not email:
                return {'message': 'Unauthorised'}, 401
            number = self.cart_db.number_total_item_add_in_cart(email)
            return {"count":number}
        except Exception as e:
            return {'message': 'Error', 'error': str(e)}, 401
