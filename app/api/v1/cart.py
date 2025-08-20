import datetime
import uuid
from flask import Blueprint, g, json, request
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response
from app.models.cart import Cart
from app.schemas.cart import Cart_Schema, Cart_filter


cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_cart', methods=['POST'])
@validate_token
def add_cart():  
    current_user = g.current_user
    data = request.json
    data['shop_owner_id'] = current_user
    insert_data = Cart_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())
    product = Cart(
        **insert_data
    )
    product.save()      

    return create_response(True,'Product added to cart',None,None,201)


@cart_bp.route('/get_cart_details', methods=['GET'])
@validate_token
def get_cart_details():  
    current_user = g.current_user

    filter={}
  
    filter['shop_owner_id'] = current_user
    
    query_filter = Cart_filter(**filter).model_dump()
    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    product = Cart.objects(**query_filter).to_json()    
    res_data  = json.loads(product)   
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@cart_bp.route('/get_cart_details_byid', methods=['GET'])
@validate_token
def get_cart_details_byid():  

    current_user = g.current_user
    request_data = request.args.to_dict()
    product = Cart.objects(_id = request_data.get('id')).first().to_json()    
    res_data  = json.loads(product)   
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@cart_bp.route('/delete_cart', methods=['DELETE'])
@validate_token
def delete_product():  
    data = request.args.to_dict()
    id = data.get("id") 

    cart = Cart.objects(_id=id).first()    
    if not cart:        
        return create_response(False,'Cart does not exists',None,None,404)
   
    cart.delete()
    return create_response(True,'Data deleted successfully',None,None,200)



@cart_bp.route('/update_cart', methods=['PUT'])
@validate_token
def update_product():  
    data = request.json
    id = data.get("id")       
    data['modified_at'] = datetime.datetime.now
    cart = Cart.objects(_id=id).first()    
    if not cart:        
        return create_response(False,'Cart does not exists',None,None,404)
    data.pop('id')
    cart.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)