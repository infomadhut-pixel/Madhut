from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.T_shirt.t_shirtDb import TshirtDatabase

blp = Blueprint('detail of particular products', __name__)


@blp.route('/admin/product/detail')
class AdminProductDetail(MethodView):
    def __init__(self):
        self.product_detail_db = TshirtDatabase()

    def post(self):
        product_id = request.args.get("product_id")
        result = self.product_detail_db.fetch_single_product_detail(product_id)
        return result
