from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask import request
from ..extensions import cache

blp = Blueprint('admin view all product', __name__)


@blp.route('/admin/view/all/product')
class AdminViewAllProduct(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()

    @cache.cached(timeout=120, query_string=True)
    def post(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        result = self.product_db.fetch_products(page, limit)
        return result
