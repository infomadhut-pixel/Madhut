from datetime import datetime

from bson import ObjectId
from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.User.check_out import OrderTshirt
from ..authorise import get_current_user
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from ..Database.User_Log_Details.user_order_logs import OrderLog

blp = Blueprint('user check out detail', __name__)


@blp.route('/order/checkout')
class CheckOutOrder(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()
        self.tshirt_db = TshirtDatabase()
        self.order_log = OrderLog()

    def post(self):
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401
        data = request.get_json()
        product_id = data['product_id']
        ip_address = request.headers.get("X-FORWARDED-FOR", request.remote_addr)
        user_agent = request.user_agent.string
        activity_response = {
            "action": "CHECKOUT_STATRTED",
            "email": email,
            "products": product_id,
            "total_amount": data['total_amount'],
            "payment_method": data['payment_mode'],
            "ip_address": ip_address,
            'device': user_agent,
            "time": datetime.utcnow()
        }
        self.order_log.save_order_log(activity_response)
        quantity_ = data['quantity']
        result = self.order_db.create_order(email, data)
        self.tshirt_db.update_stock(ObjectId(product_id), quantity_)
        return result
