from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from ..extensions import cache

blp = Blueprint('tshirt', __name__)


@blp.route('/user/tshirts')
class FetchTshirt(MethodView):
    def __init__(self):
        self.tshirt_db = TshirtDatabase()

    @cache.cached(timeout=120, query_string=True)
    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 15))
        min_price = request.args.get('minPrice')
        max_price = request.args.get('maxPrice')
        if min_price and max_price:
            min_price = float(min_price)
            max_price = float(max_price)
        result = self.tshirt_db.fetch_product(page, limit, min_price, max_price)
        return jsonify(result)
