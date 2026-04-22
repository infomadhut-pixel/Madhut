from flask_smorest import Blueprint
from flask.views import MethodView
from ..Database.T_shirt.t_shirtDb import TshirtDatabase
from flask import request, jsonify

blp = Blueprint('user filter tshirt through its variety', __name__)


@blp.route('/tshirt/variety')
class TshirtVariety(MethodView):
    def __init__(self):
        self.tshirt_db = TshirtDatabase()

    def get(self):
        try:
            tshirt_variety = request.args.get('type')
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            skip = (page - 1) * limit
            data = self.tshirt_db.tshirt_variety_get_tshirt(tshirt_variety, skip, limit)
            return data
        except Exception as e:
            return jsonify(str(e))
