import uuid
from flask import Blueprint, g, json, request
from app.api.v1.order_tracking import create_order_tracking
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response, generate_uniform_unique_id
from app.models.category import Category
from app.models.order import Order
from app.models.order_tracking import Order_Tracking
from app.models.ordered_product import Ordered_product
from app.models.product import Product
from app.models.shop import Shop
from app.models.shop_owner import Shop_owner
from app.schemas.order import Order_Schema, Order_filter
from app.schemas.order_tracking import Order_Tracking_Schema
from app.schemas.ordered_product import Ordered_product_Schema

order_bp = Blueprint('order', __name__)

@order_bp.route('/create_order', methods=['POST'])
@validate_token
def create_order():  
    current_user = g.current_user
    data = request.json

    shop_owner = Shop_owner.objects(_id = current_user).first()

    
    # product_data = data.get('product_details')

    # product = Product.objects(_id = product_data['product_id']).first()    

    # if not product:        
    #     return create_response(False,'product not found',None,None,404)
    
    # total_quantity = product.available_quantity
    # order_quantity = product_data['product_quantity']
    # remaining_quantity = int(total_quantity) - int(order_quantity)
    # product = Product.objects(_id=product_data['product_id']).first()
    # if not product:
    #     return create_response(False,'Product not found',None,None,404)
    
    data['shop_owner_id'] = current_user
    data['shop_id'] = shop_owner['shop_id']
    data['vendor_owner_id'] = shop_owner['vendor_id']
    data['order_unique_id'] = generate_uniform_unique_id("ORD")
    insert_data = Order_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())    

    # product_data['order_id'] = insert_data['_id'] 
    # ordered_product_details = Ordered_product_Schema(**product_data).model_dump()
    # ordered_product_details['_id'] = str(uuid.uuid4())            

    order = Order(
        **insert_data
    )
    order.save()

    # ordered_product = Ordered_product(
    #     **ordered_product_details
    # )
    # ordered_product.save()

    order_tracking_data={
        "order_id": order.id,
        "status" :"order placed",
        "description": "order placed"
    }
    insert_order_tracking = create_order_tracking(order_tracking_data)
    # insert_order_tracking_data = Order_Tracking_Schema(**order_tracking_data).model_dump()
    # insert_order_tracking_data['_id'] = str(uuid.uuid4())
    # order_tracking = Order_Tracking(
    #     **insert_order_tracking_data
    # )
    # order_tracking.save()  
    # update_product_quantity = Product.objects(_id = product_data['product_id']).update(available_quantity = remaining_quantity)
    product_details = data.get('product_details')
    product_details['order_id'] = order.id
    insert_product_details = create_ordered_product(product_details)
    return create_response(True,'Order created successfully',order.id,None,201)


@order_bp.route('/get_order', methods=['GET'])
@validate_token
def get_all_order(): 
    
    current_user = g.current_user
    user_type  = g.claims.get('roles')

    request_data = request.args.to_dict()

    query_filter={}
    if user_type == 'vendor_owner':        
        request_data['vendor_owner_id'] = current_user

    if user_type == 'shop_owner':        
        request_data['shop_owner_id'] = current_user    
    query_filter = Order_filter(**request_data).model_dump()
    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    product = Order.objects(**query_filter).order_by('-createdAt').to_json()  
    res_data  = json.loads(product)    
   
    return create_response(True,'Data retrevied successfully',res_data,None,200)

@order_bp.route('/get_order_details_byid', methods=['GET'])
@validate_token
def get_cart_details_byid():  

    request_data = request.args.to_dict()
    order_details = Order.objects(_id = request_data.get('id')).first().to_json()    
    res_data  = json.loads(order_details)   
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@order_bp.route('/get_ordered_product_byid', methods=['GET'])
@validate_token
def get_ordered_product_byid():  

    request_data = request.args.to_dict()
    order_details = Ordered_product.objects(order_id = request_data.get('id')).to_json()    
    res_data  = json.loads(order_details)   
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)



@order_bp.route('/create_ordered_product', methods=['POST'])
@validate_token
def create_ordered_product(data=None):  
    current_user = g.current_user
    if not data:
        data = request.json    
    product = Product.objects(_id = data['product_id']).first()    

    if not product:        
        return create_response(False,'product not found',None,None,404)
    
    total_quantity = product.available_quantity
    order_quantity = data['product_quantity']
    remaining_quantity = int(total_quantity) - int(order_quantity)

    product = Product.objects(_id=data['product_id']).first()
    if not product:
        return create_response(False,'Product not found',None,None,404)   
   
    ordered_product_details = Ordered_product_Schema(**data).model_dump()
    ordered_product_details['_id'] = str(uuid.uuid4())            
    ordered_product = Ordered_product(
        **ordered_product_details
    )
    ordered_product.save()
    update_product_quantity = Product.objects(_id = data['product_id']).update(available_quantity = remaining_quantity)
    return create_response(True,'Product inserted successfully',ordered_product.id,None,200)



@order_bp.route('/create_multiple_product_order', methods=['POST'])
@validate_token
def create_multiple_product_order():  
    current_user = g.current_user
    data = request.json

    shop_owner = Shop_owner.objects(_id = current_user).first()
    
    
    data['shop_owner_id'] = current_user
    data['shop_id'] = shop_owner['shop_id']
    data['vendor_owner_id'] = shop_owner['vendor_id']
    data['order_unique_id'] = generate_uniform_unique_id("ORD")
    insert_data = Order_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())    
           

    order = Order(
        **insert_data
    )
    order.save()

    order_tracking_data={
        "order_id": order.id,
        "status" :"order placed",
        "description": "order placed"
    }

    insert_order_tracking = create_order_tracking(order_tracking_data)
   
    product_details = data.get('product_details')
    for product_data in product_details:
        product_data['order_id'] = order.id
        insert_product_details = create_ordered_product(product_data)

    return create_response(True,'Order created successfully',order.id,None,201)