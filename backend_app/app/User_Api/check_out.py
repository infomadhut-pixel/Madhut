from bson import ObjectId
from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.User.check_out import OrderTshirt
from ..authorise import get_current_user
from ..Database.T_shirt.t_shirtDb import TshirtDatabase

blp = Blueprint('user check out detail', __name__)


@blp.route('/order/checkout')
class CheckOutOrder(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()
        self.tshirt_db = TshirtDatabase()

    def post(self):
        email = get_current_user()
        data = request.get_json()
        quanity_ = data['quantity']
        product_id = data['product_id']
        result = self.order_db.create_order(email, data)
        self.tshirt_db.update_stock(ObjectId(product_id),quanity_)
        return result
