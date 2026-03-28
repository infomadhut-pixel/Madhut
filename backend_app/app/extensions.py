from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_smorest import Api
from flask_bcrypt import Bcrypt
from flask_caching import Cache
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

bcrypt = Bcrypt()

api = Api()

jwt = JWTManager()
mail = Mail()
# limiter = Limiter(
#     key_func=get_remote_address,
#     storage_uri="redis://localhost:6379"
# )


cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 120
})
