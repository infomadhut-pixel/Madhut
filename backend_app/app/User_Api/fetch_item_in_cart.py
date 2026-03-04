from flask.views import MethodView
from flask_smorest import Blueprint
from ..authorise import get_current_user
from ..Database.User.add_to_cart import AddToCart

blp = Blueprint('fetch item detail in cart', __name__)


@blp.route('/user/fetch/item/detail/in/cart')
class FetchItemDetailInCart(MethodView):
    def __init__(self):
        self.item_db = AddToCart()

    def get(self):
        email = get_current_user()
        response = self.item_db.fetch_item_in_cart(email)
        return response
