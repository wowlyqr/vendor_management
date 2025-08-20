import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "supersecret")
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'superjwtsecret')
    MONGODB_SETTINGS = {
        'host': "mongodb+srv://user:GkqHBho0GoMi5IZB@wowelse1.c179k.mongodb.net/vendor?retryWrites=true&w=majority&appName=wowelse1"
        # 'host': os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/vendor_db')
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://user:GkqHBho0GoMi5IZB@wowelse1.c179k.mongodb.net/vendor?retryWrites=true&w=majority&appName=wowelse1'
    }