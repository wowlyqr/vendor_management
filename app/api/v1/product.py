import datetime
import uuid
from flask import Blueprint, g, json, request
from app.decorators.auth import  validate_token
from app.helpers.utils import create_response, generate_uniform_unique_id
from app.models.category import Category
from app.models.product import Product
from app.models.shop_owner import Shop_owner
from app.schemas.category import Pant_Category_Schema, Shirt_Category_Schema
from app.schemas.product import Product_Schema, Product_filter

product_bp = Blueprint('product', __name__)

@product_bp.route('/create_product', methods=['POST'])
@validate_token
def create_product():  
    current_user = g.current_user
    data = request.form.to_dict() 
    data['vendor_owner_id'] = current_user
    data['product_unique_id'] = generate_uniform_unique_id("PRD")
    insert_data = Product_Schema(**data).model_dump()
    insert_data['_id'] = str(uuid.uuid4())
    product = Product(
        **insert_data
    )
    product.save()
    # if data['category'].lower() == 'pant':
    #     category_data = {
    #         'category':data['category'],
    #         'pant_size': data['pant_size'],
    #         'pant_colour': data['pant_colour'],
    #         'pant_price': data['pant_price'],
    #         'product_id': product.id,
    #         'quantity': data['quantity'],       
    #     }
    #     insert_category_data = Pant_Category_Schema(**category_data).model_dump()       

    # else:
    #     category_data = {
    #         'category':data['category'],
    #         'shirt_size': data['shirt_size'],
    #         'shirt_colour': data['shirt_colour'],
    #         'shirt_price': data['shirt_price'],
    #         'product_id': product.id,
    #         'quantity': data['quantity'],          
    #     }
    #     insert_category_data = Shirt_Category_Schema(**category_data).model_dump()

    # insert_category_data['_id'] = str(uuid.uuid4())
    # insert_category_data['vendor_owner_id'] = current_user
    # category = Category(**insert_category_data)
    # category.save()

    # update_primary_category_data = Product.objects(_id=product.id).update(primary_product_id=category.id)    

    return create_response(True,'Product created successfully',None,None,201)


@product_bp.route('/update_product', methods=['PUT'])
@validate_token
def update_product():  
    data = request.form.to_dict()
    id = data.get("id")       
    data['modified_at'] = datetime.datetime.now
    product = Product.objects(_id=id).first()    
    if not product:        
        return create_response(False,'Product does not exists',None,None,404)
    data.pop('id')
    product.update(**data)
    return create_response(True,'Data updated successfully',None,None,200)


@product_bp.route('/get_product', methods=['GET'])
@validate_token
def get_all_product():  
    current_user = g.current_user
    user_type  = g.claims.get('roles')
    request_data = request.args.to_dict()

    query_filter={}
    if user_type == 'vendor_owner':
        request_data['vendor_owner_id'] = current_user

    if user_type == 'shop_owner':
        shop_owner = Shop_owner.objects(_id = current_user).first()
        request_data['vendor_owner_id'] = shop_owner.vendor_id

    query_filter = Product_filter(**request_data).model_dump()
    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    product = Product.objects(**query_filter).to_json()    
    res_data  = json.loads(product)
    # response_data = []
    # for data in res_data:
    #     category_list = Category.objects(_id = data['primary_product_id']).first().to_json()    
    #     if category_list:
    #         category = json.loads(category_list)
    #         data['primary_category_list'] = category
    #     response_data.append(data)
  
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@product_bp.route('/get_product_byid', methods=['GET'])
@validate_token
def get_product_byid():  
    request_data = request.args.to_dict()
    id = request_data.get('id')
    product = Product.objects(_id=id).first().to_json()    
    if not product:
        return create_response(False,'Product does not exists',None,None,404)
    res_data = json.loads(product)
    # category_list = Category.objects(_id = res_data['primary_product_id']).first().to_json()    
    # if category_list:
    #     category = json.loads(category_list)
    #     res_data['primary_category_list'] = category
    return create_response(True,'Data retrevied successfully',res_data,None,200)


@product_bp.route('/delete_product', methods=['DELETE'])
@validate_token
def delete_product():  
    data = request.args.to_dict()
    id = data.get("id") 

    product = Product.objects(_id=id).first()    
    if not product:        
        return create_response(False,'Product does not exists',None,None,404)
   
    product.delete()
    return create_response(True,'Data deleted successfully',None,None,200)




@product_bp.route('/insert_bulk_product', methods=['POST'])
@validate_token
def insert_bulk_product():  
    
    import pandas as pd

    # file = request.files['file']
    # df = pd.read_excel(file)
    # # Load the Excel file
    # # df = pd.read_excel('sample_data.xlsx')  # Replace with your Excel file path

    # # Convert to list of dictionaries
    # data = df.to_dict(orient='records')

    # # Print the result
    # print(data)

    
    file = request.files['file']
    df = pd.read_excel(file)
    data_list = df.to_dict(orient='records')

    current_user = g.current_user

    all_products = []
    all_categories = []

    for data in (data_list):
        try:
            data['vendor_owner_id'] = current_user

            category_id = str(uuid.uuid4())

            product_data = Product_Schema(**data).model_dump()
            product_data['_id'] = str(uuid.uuid4())
            product = Product(**product_data)

            product['primary_product_id'] = category_id

            if data['category'].lower() == 'pant':

                category_data = {
                    'category': data['category'],
                    'pant_size': data['pant_size'],
                    'pant_colour': data['pant_colour'],
                    'pant_price': data['pant_price'],
                    'product_id': product_data['_id'],
                    'quantity': data['quantity']
                }
                insert_category_data = Pant_Category_Schema(**category_data).model_dump()

            else:
                category_data = {
                    'category': data['category'],
                    'shirt_size': data['shirt_size'],
                    'shirt_colour': data['shirt_colour'],
                    'shirt_price': data['shirt_price'],
                    'product_id': product_data['_id'],
                    'quantity': data['quantity']
                }
                insert_category_data = Shirt_Category_Schema(**category_data).model_dump()

            insert_category_data['_id'] = category_id
            insert_category_data['vendor_owner_id'] = current_user
            category = Category(**insert_category_data)

            # Append only if no validation errors
            all_products.append(product)
            all_categories.append(category)

        except Exception as e:
            return create_response(False,f"Validation failed at row : {str(e)}",None,str(e),400)
        
    product = Product.objects.insert(all_products)
    category  = Category.objects.insert(all_categories)
    
    return create_response(True,'Bulk insert successful',None,None,200)