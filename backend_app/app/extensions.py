from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_smorest import Api
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


api = Api()

jwt = JWTManager()
mail = Mail()
