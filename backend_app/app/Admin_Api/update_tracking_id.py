from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.User.check_out import OrderTshirt

blp = Blueprint('admin update tracking id', __name__)

@blp.route('/admin/add/tracking')
class UpdateTrackingId(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()

    def put(self):
        data = request.get_json()
        order_id = data['order_id']
        tracking_id = data['tracking_id']
        response = self.order_db.update_tracking_id(order_id, tracking_id)
        return response
