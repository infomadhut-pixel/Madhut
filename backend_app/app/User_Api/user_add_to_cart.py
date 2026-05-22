from datetime import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.add_to_cart import AddToCart
from ..authorise import get_current_user
from ..Database.User_Log_Details.user_add_to_cart_logs import UserAddToCartLog


blp = Blueprint('add items in cart', __name__)


@blp.route('/user/add/item/cart')
class AddItemCart(MethodView):
    def __init__(self):
        self.add_cart_db = AddToCart()
        self.cart_log = UserAddToCartLog()

    def post(self):
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401
        data = request.get_json()
        product_id = data['product_id']

        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0]
        activity = {
            'email': email,
            "ip_address": ip_address,
            "action": 'ADD_TO_CART',
            "product_id": product_id,
            "time": datetime.utcnow()
        }
        self.cart_log.save_add_tp_cart_log(activity)
        color = data['color']
        price = data['price']
        quantity = data['quantity']
        size = data['size']
        image = data['image']
        result = self.add_cart_db.add_to_cart(email, product_id, color, price, quantity, size, image)
        return result
