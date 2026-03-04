from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_smorest import Api
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

bcrypt = Bcrypt()

api = Api()

jwt = JWTManager()
mail = Mail()
# limiter = Limiter(
#     key_func=get_remote_address,
#     storage_uri="redis://localhost:6379"
# )
