import uuid
from flask import Blueprint, g, json, request, jsonify
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response
from app.models.order import Order
from app.models.order_tracking import Order_Tracking
from app.schemas.order_tracking import Order_Tracking_Schema

order_tracking_bp = Blueprint('order_tracking', __name__)

@order_tracking_bp.route('/create_order_tracking', methods=['PUT'])
@validate_token
def create_order_tracking(data=None):  
    current_user = g.current_user
    if not data:
        data = request.json
    order = Order.objects(_id = data['order_id']).first()
    if not order:
        return create_response(False,'Order does not exists',None,None,404)    

    insert_data = Order_Tracking_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())
    order_tracking = Order_Tracking(
        **insert_data
    )
    order_tracking.save()  
    update_order_status = Order.objects(_id = data['order_id']).update(status = data['status'])

    return create_response(True,'Order tracking created successfully',None,None,201)


@order_tracking_bp.route('/get_order_tracking_byorderid', methods=['GET'])
@validate_token
def get_order_tracking_byorderid(): 
    current_user = g.current_user 
    data = request.args.to_dict()
    order_tracking = Order_Tracking.objects(order_id = data['order_id']).to_json()    
    res_data  = json.loads(order_tracking)
    return create_response(True,'Data retrevied successfully',res_data,None,200)

