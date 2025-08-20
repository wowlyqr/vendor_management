import datetime
import uuid
from flask import Blueprint, g, json, render_template, request, jsonify
from pydantic import BaseModel
from werkzeug.security import generate_password_hash
from app.decorators.auth import  validate_token
from app.helpers.email import send_mail
from app.helpers.utils import create_response, generate_uniform_unique_id
from app.models.credentials import Credentials
from app.models.shop import Shop
from app.models.shop_owner import Shop_owner
from app.schemas.credentials import Credentials_Schema
from app.schemas.shop import Shop_Schema
from app.schemas.shop_owner import Shop_owner_Schema, Shop_owner_filter
import pandas as pd

shop_owner_bp = Blueprint('shop_owner', __name__)

@shop_owner_bp.route('/create_shop_owner', methods=['POST'])
@validate_token
def create_shop_owner():  
    current_user = g.current_user
    data = request.json
    shop = Shop.objects(_id=data['shop_id'])
    if not shop:
        return create_response(False,'Shop does not exists',None,None,404)
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password
    data['vendor_id'] = current_user
    insert_data = Shop_owner_Schema(**data).model_dump()

    if Credentials.objects(email=data['email']).first():
        return create_response(False,'Username or email already exists',None,None,409)
    insert_data['_id'] = str(uuid.uuid4())
    shop_owner = Shop_owner(
        **insert_data
    )
    shop_owner.save()

    credentials_data = {
        'user_type': 'shop_owner',
        'email' : data['email'],
        'mobile' : data['mobile'],
        'password' :hashed_password, # Store hashed password!
        'country_code' : data['country_code'],
        'user_id':shop_owner.id
        }
    
    insert_credentials_data = Credentials_Schema(**credentials_data).model_dump()
    insert_credentials_data['_id'] = str(uuid.uuid4())
    credentials_doc = Credentials(**insert_credentials_data)
    credentials_doc.save()
    return create_response(True,'Shop owner created successfully',None,None,201)


@shop_owner_bp.route('/update_shop_owner', methods=['PUT'])
@validate_token
def update_shop_owner():  
    data = request.json
    id = data.get("id")
    # update_data = Update_shop_owner_Schema(**data).model_dump()
       
    data['modified_at'] = datetime.datetime.now

    shop_owner = Shop_owner.objects(_id=id).first()
    
    if not shop_owner:   
        return create_response(False,'Shop owner does not exists',None,None,404)     
    
    data.pop('id')
    shop_owner.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)


@shop_owner_bp.route('/get_shop_owner', methods=['GET'])
@validate_token
def get_shop_owner():  
    request_data = request.args.to_dict()
    
    query = Shop_owner_filter(**request_data).model_dump()
    query = {k: v for k, v in query.items() if v is not None}
    
    shop_owner = Shop_owner.objects(**query).to_json()
    response_data = json.loads(shop_owner)
    return create_response(True,'Data retrevied successfully',response_data,None,200)


@shop_owner_bp.route('/get_shop_owner_byid', methods=['GET'])
@validate_token
def get_shop_owner_byid():  
    request_data = request.args.to_dict()
    id = request_data.get('id')
    shop_owner = Shop_owner.objects(_id=id).first().to_json()
    if not shop_owner:
        return create_response(False,'Shop owner does not exists',None,None,404)
    response_data = json.loads(shop_owner)
    return create_response(True,'Data retrevied successfully',response_data,None,200)


@shop_owner_bp.route('/get_shopowner_byshop_id', methods=['GET'])
@validate_token
def get_shop_owner_byshop_id():  
    request_data = request.args.to_dict()
    id = request_data.get('shop_id')
    shop_owner = Shop_owner.objects(shop_id=id).to_json()
    if not shop_owner:
        return create_response(False,'Shop owner does not exists',None,None,404)
    response_data = json.loads(shop_owner)
    return create_response(True,'Data retrevied successfully',response_data,None,200)

@shop_owner_bp.route('/create_shopowner_shop', methods=['POST'])
@validate_token
def create_shopowner_and_shop():  
    current_user = g.current_user
    data = request.json
    shop_details = data.get('shop_details')
    shop_details['vendor_owner_id']=current_user    
    shop_details['shop_unique_id']=generate_uniform_unique_id("SP")
    insert_shop_data = Shop_Schema(**shop_details).model_dump()
    insert_shop_data['_id'] = str(uuid.uuid4())
    shop = Shop(
        **insert_shop_data
    )
    shop.save()

    shop_owner_data = data.get('shop_owner_details')
    old_password = shop_owner_data['password']
    hashed_password = generate_password_hash(shop_owner_data['password'])
    shop_owner_data['password'] = hashed_password
    shop_owner_data['vendor_id'] = current_user
    shop_owner_data['shop_id'] = shop.id
    insert_shopowner_data = Shop_owner_Schema(**shop_owner_data).model_dump()

    if Credentials.objects(email=shop_owner_data['email']).first():
        return create_response(False,'Username or email already exists',None,None,409)

    insert_shopowner_data['_id'] = str(uuid.uuid4())
    shop_owner = Shop_owner(
        **insert_shopowner_data
    )
    shop_owner.save()

    credentials_data = {
        'user_type': 'shop_owner',
        'email' : shop_owner_data['email'],
        'mobile' : shop_owner_data['mobile'],
        'password' :hashed_password, # Store hashed password!
        'country_code' : shop_owner_data['country_code'],
        'user_id':shop_owner.id
        }
    
    insert_credentials_data = Credentials_Schema(**credentials_data).model_dump()
    insert_credentials_data['_id'] = str(uuid.uuid4())
    credentials_doc = Credentials(**insert_credentials_data)
    credentials_doc.save()

    html_template = render_template('welcome_email_template.html',email=shop_owner_data['email'],password=old_password,login_url='http://vendor-management-wowelse.s3-website-us-east-1.amazonaws.com/auth/sign-in')
    welcome_mail  = send_mail(shop_owner_data['email'],"Welcome aboard! Access your account now",html_template,'wowlyqr@gmail.com')
    
    return create_response(True,'Shop and shop owner created successfully',None,None,201)



@shop_owner_bp.route('/insert_bulk_shop_details', methods=['POST'])
@validate_token
def insert_bulk_shop_details():  
    

    file = request.files['file']
    df = pd.read_excel(file)
    data_list = df.to_dict(orient='records')

    current_user = g.current_user

    shop_data = []
    shop_owner_data = []
    credentials_data = []

    for data in (data_list):
        try:

            #Shop details
            shop_details = {}
            shop_details['shop_name']  = data.get('shop_name')
            shop_details['shop_unique_id'] = generate_uniform_unique_id("SP")
            shop_details['expected_open_date']= str(data.get('expected_open_date'))
            shop_details['vendor_owner_id'] = current_user
            shop_details['address']= data.get('address')
            shop_details['city']= data.get('city')
            shop_details['state']= data.get('state')
            shop_details['pincode']= data.get('pincode')

            insert_shop_data = Shop_Schema(**shop_details).model_dump()
            insert_shop_data['_id'] = str(uuid.uuid4())

            #Shop owner details
            shop_owner_details = {}
            hashed_password = generate_password_hash(data.get('password'))
            shop_owner_details['password'] = hashed_password
            shop_owner_details['vendor_id'] = current_user
            shop_owner_details['shop_id'] = insert_shop_data['_id']
            shop_owner_details['name'] = data.get('name')
            shop_owner_details['gender']= data.get('gender')
            shop_owner_details['password']= hashed_password
            shop_owner_details['aadhar_number'] = str(data.get('aadhar_number'))
            shop_owner_details['email']= data.get('email')
            shop_owner_details['mobile']= data.get('mobile')
            shop_owner_details['country_code']= data.get('country_code')          

            insert_shopowner_data = Shop_owner_Schema(**shop_owner_details).model_dump()
            insert_shopowner_data['_id'] = str(uuid.uuid4())           

            #credentials details
            if Credentials.objects(email=shop_owner_details['email']).first():
                return create_response(False,'Username or email already exists',None,None,409)

            credentials_details = {
                'user_type': 'shop_owner',
                'email' : shop_owner_details['email'],
                'mobile' : shop_owner_details['mobile'],
                'password' :hashed_password, # Store hashed password!
                'country_code' : shop_owner_details['country_code'],
                'user_id':insert_shopowner_data['_id']
                }
            
            insert_credentials_data = Credentials_Schema(**credentials_details).model_dump()
            insert_credentials_data['_id'] = str(uuid.uuid4())            

            #append data 
            shop_obj = Shop(**insert_shop_data)
            shop_owner_obj = Shop_owner(**insert_shopowner_data)
            credentials_obj = Credentials(**insert_credentials_data)

            shop_data.append(shop_obj)
            shop_owner_data.append(shop_owner_obj)
            credentials_data.append(credentials_obj)

        except Exception as e:
            return create_response(False,f"Validation failed at row : {str(e)}",None,str(e),400)
  
    shop = Shop.objects.insert(shop_data)
    shop_owner  = Shop_owner.objects.insert(shop_owner_data)
    credentials  = Credentials.objects.insert(credentials_data)
    
    return create_response(True,'Shop and shop owner inserted successful',None,None,200)