from mongoengine import Document, StringField, IntField, DateTimeField,FloatField,ListField
import datetime

class Product(Document):
    meta = {'strict': False}
    _id = StringField(primary_key=True,required=True)
    product_unique_id = StringField(required=True)
    name = StringField(required=True)
    image = StringField(required=False)
    category = StringField(required=True)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)    
    vendor_owner_id = StringField(required=True)
    primary_product_id = StringField(required=False)
    description = StringField(required=False,default=None)
    modified_at = DateTimeField(default=None)
    price =  FloatField(required=False)
    available_sizes = StringField(required=False)
    available_colors = StringField(required=False)
    available_quantity = IntField(required=False)
