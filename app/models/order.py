from mongoengine import Document, StringField, IntField, DateTimeField,ListField,FloatField
import datetime

class Order(Document):
    _id = StringField(primary_key=True,required=True)
    order_unique_id = StringField(required=True)
    delivery_address = StringField(required=True)
    mobile = IntField(required=True)
    pincode = IntField(required=True)   
    createdAt = DateTimeField(default=datetime.datetime.now)
    total_amount = FloatField(required=True)
    total_quantity = IntField(required=True)
    shop_owner_id = StringField(required=True)
    shop_id = StringField(required=False)
    vendor_owner_id = StringField(required=True)
    status = StringField(required=True)

