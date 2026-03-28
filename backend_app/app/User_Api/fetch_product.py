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
        limit = int(request.args.get('limit', 5))
        result = self.tshirt_db.fetch_products(page, limit)
        return jsonify(result)
