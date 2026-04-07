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

    @cache.cached(timeout=60, query_string=True)
    def get(self):

        last_id = request.args.get('last_id', None)

        try:
            limit = int(request.args.get('limit', 20))
        except:
            limit = 20

        result = self.product_db.fetch_products(last_id, limit)

        return result, 200
