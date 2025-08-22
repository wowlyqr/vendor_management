import datetime
import uuid
from flask import Blueprint, json, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from app.decorators.auth import  validate_token
from app.helpers.email import send_mail
from app.helpers.utils import create_response
from app.models.credentials import Credentials
from app.models.vendor_owner import Vendor_owner
from app.schemas.credentials import Credentials_Schema
from app.schemas.vendor_owner import  Vendor_owner_Schema, Vendor_owner_filter

vendor_owner_bp = Blueprint('vendor_owner', __name__)

@vendor_owner_bp.route('/create_vendor_owner', methods=['POST'])
@validate_token
def create_vendor_owner():    
    data = request.json
    old_password = data['password']
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    insert_data = Vendor_owner_Schema(**data).model_dump()

    if Credentials.objects(email=data['email']).first():
        return create_response(False,'Username or email already exists',None,None,409)
    insert_data['_id'] = str(uuid.uuid4())
    vendor_owner = Vendor_owner(
        **insert_data
    )
    vendor_owner.save()

    credentials_data = {
        'user_type': 'vendor_owner',
        'email' : data['email'],
        'mobile' : data['mobile'],
        'password' :hashed_password,# Store hashed password!
        'country_code' : data['country_code'],
        'user_id':vendor_owner.id
        }

    insert_credentials_data = Credentials_Schema(**credentials_data).model_dump()
    insert_credentials_data['_id'] = str(uuid.uuid4())
    credentials = Credentials(**insert_credentials_data)
    credentials.save()
    html_template = render_template('welcome_email_template.html',email=data.get('email'),password=old_password,login_url='http://vendor-management-wowelse.s3-website-us-east-1.amazonaws.com/auth/sign-in')
    welcome_mail  = send_mail(data.get('email'),"Welcome aboard! Access your account now",html_template,'wowlyqr@gmail.com')
    return create_response(True,'Vendor owner created successfully',None,None,201)


@vendor_owner_bp.route('/update_vendor_owner', methods=['PUT'])
@validate_token
def update_vendor_owner():  
    data = request.json
    id = data.get("id")
    # update_data = Update_Vendor_owner_Schema(**data).model_dump()
       
    data['modified_at'] = datetime.datetime.now

    vendor_owner = Vendor_owner.objects(_id=id).first()
    
    if not vendor_owner:       
        return create_response(False,'Vendor owner does not exists',None,None,404) 
    if data['password']:
        hashed_password = generate_password_hash(data['password'])
        data['password'] = hashed_password
    data.pop('id')
    vendor_owner.update(**data)
    if data['password']:
        update_credentials = Credentials.objects(user_id = id).update(password = hashed_password)

    return create_response(True,'Data updated successfully',None,None,200) 
    


@vendor_owner_bp.route('/get_vendor_owner', methods=['GET'])
@validate_token
def get_vendor_owner():  

    request_data = request.args.to_dict()
    
    query = Vendor_owner_filter(**request_data).model_dump()
    query = {k: v for k, v in query.items() if v is not None}
    
    vendor_owner = Vendor_owner.objects(**query).to_json()
    response_data = json.loads(vendor_owner)
    return create_response(True,'Data updated successfully',response_data,None,200) 


@vendor_owner_bp.route('/get_vendor_owner_byid', methods=['GET'])
@validate_token
def get_vendor_owner_byid():  
    request_data = request.args.to_dict()
    id = request_data.get('id')
    vendor_owner = Vendor_owner.objects(_id=id).first()
    if not vendor_owner:
        return create_response(False,'Vendor owner does not exists',None,None,404) 
    response_data = json.loads(vendor_owner.to_json())
    return create_response(True,'Data retrevied successfully',response_data,None,200) 
