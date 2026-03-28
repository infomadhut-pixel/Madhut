from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.check_out import OrderTshirt

blp = Blueprint("admin seen all orders", __name__)


@blp.route('/admin/seen/all/order')
class AllOrders(MethodView):
    def __init__(self):
        self.all_order = OrderTshirt()

    def post(self):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
        skip=(page-1)*limit
        response = self.all_order.fetch_order(skip=skip,limit=limit)
        return response
