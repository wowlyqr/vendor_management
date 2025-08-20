from flask import jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from mongoengine.errors import ValidationError as MongoValidationError, NotUniqueError

from app.helpers.utils import create_response

class APIException(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        simplified_errors = [
        {
            "loc": err["loc"],
            "msg": err["msg"],
            "type": err["type"]
        }
        for err in error.errors()
        ]
        return create_response(False,'Validation error',None,simplified_errors,400)
        

    @app.errorhandler(MongoValidationError)
    def handle_mongo_validation_error(error):
        return create_response(False,'Database validation error',None,str(error),400)
       

    @app.errorhandler(NotUniqueError)
    def handle_not_unique_error(error):
        return create_response(False,'Duplicate entry',None,str(error),400)
       

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return create_response(False,'error',None,error.description,error.code)
        

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return create_response(False,'Internal server error',None,str(error),500)
       