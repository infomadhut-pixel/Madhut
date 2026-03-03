from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.add_to_cart import AddToCart
from ..authorise import get_current_user

blp = Blueprint('add items in cart', __name__)


@blp.route('/user/add/item/cart')
class AddItemCart(MethodView):
    def __init__(self):
        self.add_cart_db = AddToCart()

    def post(self):
        email = get_current_user()
        data = request.get_json()
        product_id = data['product_id']
        color = data['color']
        price = data['price']
        quantity = data['quantity']
        size = data['size']
        image = data['image']
        result = self.add_cart_db.add_to_cart(email, product_id, color, price, quantity, size, image)
        return result
