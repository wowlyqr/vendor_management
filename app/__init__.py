from flask import Flask
from flask_cors import CORS
from app.helpers.email import init_mail
from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import socketio, limiter, jwt
import mongoengine as me
from .api.v1.user import user_bp
from .api.v1.auth import auth_bp
from .api.v1.shop_owner import shop_owner_bp
from .api.v1.shop import shop_bp
from .api.v1.vendor_owner import vendor_owner_bp
from .api.v1.product import product_bp
from .api.v1.category import category_bp
from .api.v1.order import order_bp
from .api.v1.order_tracking import order_tracking_bp
from .api.v1.cart import cart_bp
from .api.v1.brand_theme import brand_theme_bp
from .api.v1.admin import admin_bp
from .sockets.events import register_socketio_events
from .exceptions import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    me.connect(host=app.config['MONGODB_SETTINGS']['host'])
    socketio.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    CORS(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'wowlyqr@gmail.com'
    app.config['MAIL_PASSWORD'] = 'kxbv ewbh fmnb ccem'
    app.config['MAIL_DEFAULT_SENDER'] = 'wowlyqr@gmail.com'
    init_mail(app)

    register_error_handlers(app)

    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(shop_owner_bp, url_prefix='/api/v1/shop_owner')
    app.register_blueprint(shop_bp, url_prefix='/api/v1/shop')
    app.register_blueprint(vendor_owner_bp, url_prefix='/api/v1/vendor_owner')
    app.register_blueprint(product_bp, url_prefix='/api/v1/product')
    app.register_blueprint(category_bp, url_prefix='/api/v1/category')
    app.register_blueprint(cart_bp, url_prefix='/api/v1/cart')
    app.register_blueprint(order_bp, url_prefix='/api/v1/order')
    app.register_blueprint(order_tracking_bp, url_prefix='/api/v1/order_tracking')
    app.register_blueprint(brand_theme_bp, url_prefix='/api/v1/brand_theme')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    register_socketio_events(socketio)

    return app 