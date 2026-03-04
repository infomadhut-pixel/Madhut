import requests
from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.User.add_to_cart import AddToCart
from ..authorise import get_current_user

blp = Blueprint("remove item from cart", __name__)


@blp.route('/remove/item/from/cart')
class RemoveItemFromCart(MethodView):
    def __init__(self):
        self.cart_db = AddToCart()

    def delete(self):
        email = get_current_user()
        cart_id = request.args.get('cart_id')
        response = self.cart_db.remove_and_update_cart_data(email, cart_id)
        return response
