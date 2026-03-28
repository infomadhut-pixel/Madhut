from flask_smorest import Blueprint
from flask.views import MethodView
from ..authorise import get_current_user
from ..Database.User.check_out import OrderTshirt

blp = Blueprint('user seen all order', __name__)


@blp.route('/user/fetch/order')
class UserFetchOrder(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()

    def get(self):
        email = get_current_user()
        if not email:
            return {"message": "Unauthorized"}, 401
        order_data = self.order_db.fetch_all_order(email)
        return order_data
