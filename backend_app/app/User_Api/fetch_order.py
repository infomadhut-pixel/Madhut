from flask_smorest import Blueprint
from flask.views import MethodView
from ..authorise import get_current_user
from ..Database.User.check_out import OrderTshirt

blp = Blueprint('user seen all order', __name__)


@blp.route('user/fetch/order')
class UserFetchOrder(MethodView):
    def __init__(self):
        self.order_db = OrderTshirt()
