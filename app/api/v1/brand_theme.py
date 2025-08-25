import datetime
import uuid
from flask import Blueprint, g, json, request
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response, upload_file_to_s3
from app.models.brand_theme import Brand_theme
from app.schemas.brand_theme import Brand_theme_Schema

brand_theme_bp = Blueprint('brand_theme', __name__)

@brand_theme_bp.route('/add_brand_theme', methods=['POST'])
@validate_token
def add_brand_theme():  
    current_user = g.current_user
    data = request.form.to_dict()
    data['vendor_owner_id'] = current_user
    insert_data = Brand_theme_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())

    try:       
        file = request.files.get('brand_logo')
        if file:
            s3_url = upload_file_to_s3(file, folder="brand_theme")
            insert_data['brand_logo'] = s3_url
            
    except Exception as e:
        return create_response(False, "File upload failed", None,str(e), 500)
    
    brand_theme = Brand_theme(
        **insert_data
    )
    brand_theme.save()      

    return create_response(True,'Theme added successfully',None,None,201)


@brand_theme_bp.route('/get_branch_theme_details', methods=['GET'])
@validate_token
def get_branch_theme_details():  
    current_user = g.current_user
    brand_theme = Brand_theme.objects(vendor_owner_id = current_user).first()
    if not brand_theme:
        return create_response(False,"Theme does not exists",None,None,404)
    response_data = json.loads(brand_theme.to_json())
  
    return create_response(True,'Data retrevied successfully',response_data,None,200)



@brand_theme_bp.route('/update_brand_theme', methods=['POST'])
@validate_token
def update_brand_theme():  
    data = request.form.to_dict()
    current_user = g.current_user
    # id = data.get("id")       
    data['modified_at'] = datetime.datetime.now
    brand_theme = Brand_theme.objects(vendor_owner_id=current_user).first()    
    if not brand_theme:        
        return create_response(False,'Theme does not exists',None,None,404)
    # data.pop('id')
    
    try:       
        file = request.files.get('brand_logo')
        if file:
            s3_url = upload_file_to_s3(file, folder="brand_theme")
            data['brand_logo'] = s3_url            
    except Exception as e:
        return create_response(False, "File upload failed", None,str(e), 500)
    
    brand_theme.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)