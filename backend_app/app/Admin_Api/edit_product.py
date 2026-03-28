from flask.views import MethodView
from flask_smorest import Blueprint
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask import request

blp = Blueprint('edit product details', __name__)


@blp.route("/admin/edit/product/detail")
class AdminEditProductDetail(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()

    def put(self):
        data = request.get_json()
        product_id = request.args.get('product_id')
        product_data = self.product_db.fetch_single_product_detail(product_id)
        data.pop('product_id', None)
        if 'sizes' in data:
            data['sizes'] = [s.strip() for s in data['sizes']]
        if 'colors' in data:
            data['colors'] = [s.strip() for s in data['colors']]
        price = data.get('price', product_data['price'])
        old_price = data.get('old_price', product_data['old_price'])
        if old_price and old_price > 0:
            discount = round(((old_price - price) / old_price) * 100)
        else:
            discount = 0
        data['discount_percent'] = discount
        response = self.product_db.update_product_detail(product_id, data)
        return response
