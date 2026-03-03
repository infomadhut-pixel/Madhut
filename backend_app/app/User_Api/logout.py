from flask import jsonify

from .Blocklist import Blocklist
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt, unset_jwt_cookies

blp = Blueprint('user logout', __name__, description='calling this api user logout.....')


@blp.route('/user/logout')
class PatientLogout(MethodView):
    @jwt_required(locations=['headers'])
    def post(self):
        jti = get_jwt()['jti']
        Blocklist.add(jti)
        response = jsonify({"message": 'user logout successfully...'})
        unset_jwt_cookies(response)
        return response, 200
