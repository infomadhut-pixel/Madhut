from flask_smorest import Blueprint
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask.views import MethodView
from flask import request
from datetime import datetime
from ..Database.User_Log_Details.user_product_view import ProductViewLog

blp = Blueprint("specific product detail", __name__)


@blp.route('/user/product/detail/')
class SpecificProductDetail(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()
        self.product_view = ProductViewLog()

    def get(self):
        id_ = request.args.get('productId')
        ip_address = request.headers.get(
            "X-Forwarded-For",
            request.remote_addr
        ).split(",")[0]
        activity_response = {
            "action": "product viewed",
            "product_id": id_,
            "ip_address": ip_address,
            "time": datetime.utcnow()
        }
        self.product_view.save_product_view_log(activity_response)

        result = self.product_db.fetch_single_product_detail(id_)
        return result
