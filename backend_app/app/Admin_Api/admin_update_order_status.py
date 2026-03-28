from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.check_out import OrderTshirt
from flask import request
from app.extensions import socketio

blp = Blueprint('admin update status of order', __name__)


@blp.route('/admin/update/status/order')
class UpdateOrderStatus(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()

    def put(self):
        data = request.get_json()
        order_id = data['order_id']
        status = data['status']
        response, code = self.order_db.update_order_status(order_id, status)
        socketio.emit("order_updated", {
            "order_id": order_id,
            "status": status
        })
        return response, code
