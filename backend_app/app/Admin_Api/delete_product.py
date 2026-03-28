from flask.views import MethodView
from flask_smorest import Blueprint

from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask import request
from app.extensions import socketio

blp = Blueprint('admin delete product', __name__)


@blp.route('/admin/delete/product')
class AdminDeleteProduct(MethodView):
    def __init__(self):
        self.product_db = TshirtDatabase()

    def delete(self):
        product_id = request.args.get('product_id')
        response, status = self.product_db.delete_product(product_id)
        if status == 200:
            socketio.emit("delete_product", {"_id": product_id})
        return response, status
