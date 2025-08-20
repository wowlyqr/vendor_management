from mongoengine import Document, StringField, DateTimeField,ListField,FloatField
import datetime

class Cart(Document):
    _id = StringField(primary_key=True,required=True)    
    product_id = StringField(required=True) 
    product_name = StringField(required=True) 
    category = StringField(required=True) 
    price = FloatField(required=True) 
    selected_product_details = ListField(required=True) 
    shop_owner_id = StringField(required=True) 
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    modified_at = DateTimeField(default=None)

  