# from flask_mongoengine import MongoEngine
# from flask_socketio import SocketIO
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from flask_jwt_extended import JWTManager

# db = MongoEngine()
# socketio = SocketIO(cors_allowed_origins="*")
# limiter = Limiter(key_func=get_remote_address)
# jwt = JWTManager() 



import mongoengine as me
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

socketio = SocketIO(cors_allowed_origins="*")
limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
