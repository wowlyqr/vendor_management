from mongoengine import Document, StringField, IntField, DateTimeField,ListField,FloatField
import datetime

class Ordered_product(Document):
    _id = StringField(primary_key=True,required=True)   
    product_id = StringField(required=True)  
    product_image = StringField(required=False)
    product_name = StringField(required=False)
    category = StringField(required=False)
    selected_product_details = ListField(required=True)
    createdAt = DateTimeField(default=datetime.datetime.now)
    product_amount = FloatField(required=True)
    product_quantity = IntField(required=True)
    order_id = StringField(required=True)
    
