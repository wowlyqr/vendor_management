import datetime
import uuid
from flask import Blueprint, g, json, request, jsonify
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response, generate_uniform_unique_id
from app.models.shop import Shop
from app.models.shop_owner import Shop_owner
from app.schemas.shop import Shop_Schema, Shop_filter

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/create_shop', methods=['POST'])
@validate_token
def create_shop():  
    current_user = g.current_user
    data = request.json 
    data['vendor_owner_id']=current_user
    data['shop_unique_id']=generate_uniform_unique_id("SP")
    insert_data = Shop_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())
    shop = Shop(
        **insert_data
    )
    shop.save()
    return create_response(True,'Shop created successfully',None,None,201)


@shop_bp.route('/update_shop', methods=['PUT'])
@validate_token
def update_shop():  
    data = request.json
    id = data.get("id")
    # update_data = Update_shop_Schema(**data).model_dump()
       
    data['modified_at'] = datetime.datetime.now

    shop = Shop.objects(_id=id).first()
    
    if not shop:        
        return create_response(False,'Shop does not exists',None,None,404)
    data.pop('id')
    shop.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)


@shop_bp.route('/get_shop', methods=['GET'])
@validate_token
def get_all_shop():  
    current_user = g.current_user
    user_type  = g.claims.get('roles')

    request_data = request.args.to_dict()

    query_filter={}
    if user_type == 'vendor_owner':        
        request_data['vendor_owner_id'] = current_user

    if user_type == 'shop_owner':      
        shop_owner = Shop_owner.objects(_id=current_user).first()
        request_data['_id'] = shop_owner.shop_id
    query_filter = Shop_filter(**request_data).model_dump(by_alias=True)  
    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    shop= Shop.objects(**query_filter).order_by('-createdAt').to_json()
    shop_data = json.loads(shop)

    response_data = []
    for data in shop_data:
        
        shop_details = data
        
        shop_owner = Shop_owner.objects(shop_id=shop_details['_id']).order_by('-createdAt').first()
        if shop_owner:
            shop_details['shop_owner_name'] = shop_owner.name
            shop_details['shop_owner_email'] = shop_owner.email
            shop_details['shop_owner_mobile'] = shop_owner.mobile
        else:
            shop_details['shop_owner_name'] = None
            shop_details['shop_owner_email'] = None
            shop_details['shop_owner_mobile'] = None
        response_data.append(shop_details)

    return create_response(True,'Data retrevied successfully',response_data,None,200)


@shop_bp.route('/get_shop_by_id', methods=['GET'])
@validate_token
def get_shop_by_id():  
    request_data = request.args.to_dict()
    id = request_data.get('id')
    shop = Shop.objects(_id=id).first().to_json()
    response_data = json.loads(shop)
    if not shop:
        return create_response(False,'Shop does not exists',None,None,404)
    shop_owner = Shop_owner.objects(shop_id=response_data['_id']).order_by('-createdAt').first()
    if shop_owner:
        response_data['shop_owner_name'] = shop_owner.name
        response_data['shop_owner_email'] = shop_owner.email
        response_data['shop_owner_mobile'] = shop_owner.mobile
    else:
        response_data['shop_owner_name'] = None
        response_data['shop_owner_email'] = None
        response_data['shop_owner_mobile'] = None
        
    return create_response(True,'Data retrevied successfully',response_data,None,200)
