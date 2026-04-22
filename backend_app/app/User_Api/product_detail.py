from flask_smorest import Blueprint
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask.views import MethodView
from flask import request

blp = Blueprint("specific product detail", __name__)


@blp.route('/user/product/detail/')
class SpecificProductDetail(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()

    def get(self):
        id_ = request.args.get('productId')
        result = self.product_db.fetch_single_product_detail(id_)
        return result

