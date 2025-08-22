import uuid
from flask import Blueprint, g, json, request
from werkzeug.security import generate_password_hash
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response
from app.models.admin import Admin
from app.models.credentials import Credentials
from app.schemas.admin import Admin_Schema
from app.schemas.credentials import Credentials_Schema

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create_admin', methods=['POST'])
def create_shop_owner():  
    data = request.json
    
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    insert_data = Admin_Schema(**data).model_dump()

    if Credentials.objects(email=data['email']).first():
        return create_response(False,'Username or email already exists',None,None,409)
    
    insert_data['_id'] = str(uuid.uuid4())
    admin = Admin(
        **insert_data
    )
    admin.save()

    credentials_data = {
        'user_type': 'admin',
        'email' : data['email'],
        'mobile' : data['mobile'],
        'password' :hashed_password, # Store hashed password!
        'country_code' : data['country_code'],
        'user_id':admin.id
        }
    
    insert_credentials_data = Credentials_Schema(**credentials_data).model_dump()
    insert_credentials_data['_id'] = str(uuid.uuid4())
    credentials_doc = Credentials(**insert_credentials_data)
    credentials_doc.save()
    return create_response(True,'Admin created successfully',None,None,201)


@admin_bp.route('/get_admin_data', methods=['GET'])
@validate_token
def get_admin():  
    current_user = g.current_user        

    admin = Admin.objects(_id = current_user).first()
    if not admin:
        return create_response(False,"Admin does not exists",None,None,404)
    response_data = json.loads(admin.to_json())
    return create_response(True,'Data retrevied successfully',response_data,None,200)