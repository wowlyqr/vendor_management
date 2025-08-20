import datetime
import uuid
from flask import Blueprint, g, json, request, jsonify
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import Pant_Category_Schema, Shirt_Category_Schema

category_bp = Blueprint('category', __name__)

@category_bp.route('/create_category', methods=['POST'])
@validate_token
def create_category():  
    current_user = g.current_user
    data = request.form.to_dict()
    check_product_exists = Product.objects(_id=data['product_id']).first()
    if not check_product_exists:
        return create_response(False,'Product does not exists',None,None,404)

    if check_product_exists['category'].lower() == 'pant':
        category_schema = Pant_Category_Schema
    else:
        category_schema = Shirt_Category_Schema

    data['category'] = check_product_exists['category']
    insert_data = category_schema(**data).model_dump()
    insert_data['vendor_owner_id'] = current_user
    insert_data['_id'] = str(uuid.uuid4())
    category = Category(
        **insert_data
    )
    category.save()
    return create_response(True,'Category created successfully',None,None,201)



@category_bp.route('/get_category_by_productid', methods=['GET'])
@validate_token
def get_product_byid():  
    request_data = request.args.to_dict()
    id = request_data.get('product_id')
    category = Category.objects(product_id=id).to_json()    
    if not category:
        return create_response(False,'Category does not exists',None,None,404)
    res_data = json.loads(category)
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@category_bp.route('/update_category', methods=['PUT'])
@validate_token
def update_category():  
    data = request.form.to_dict()
    id = data.get("id")
       
    data['modified_at'] = datetime.datetime.now

    category = Category.objects(_id=id).first()
    if not category:
        return create_response(False,'Category not found',None,None,404)
      
    data.pop('id')
    category.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)
