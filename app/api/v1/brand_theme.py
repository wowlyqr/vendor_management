import datetime
import uuid
from flask import Blueprint, g, json, request
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response
from app.models.brand_theme import Brand_theme
from app.schemas.brand_theme import Brand_theme_Schema

brand_theme = Blueprint('brand_theme', __name__)

@brand_theme.route('/add_brand_theme', methods=['POST'])
@validate_token
def add_brand_theme():  
    current_user = g.current_user
    data = request.form.to_dict()
    data['vendor_owner_id'] = current_user
    insert_data = Brand_theme_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())
    brand_theme = Brand_theme(
        **insert_data
    )
    brand_theme.save()      

    return create_response(True,'Theme added successfully',None,None,201)


@brand_theme.route('/get_branch_theme_details', methods=['GET'])
@validate_token
def get_branch_theme_details():  
    current_user = g.current_user
    product = Brand_theme.objects(vendor_owner_id = current_user).first().to_json()   
    res_data  = json.loads(product)   
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)



@brand_theme.route('/update_brand_theme', methods=['PUT'])
@validate_token
def update_product():  
    data = request.form.to_dict()
    id = data.get("id")       
    data['modified_at'] = datetime.datetime.now
    brand_theme = Brand_theme.objects(_id=id).first()    
    if not brand_theme:        
        return create_response(False,'Theme does not exists',None,None,404)
    data.pop('id')
    brand_theme.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)