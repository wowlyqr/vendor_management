from mongoengine import Document, StringField, DateTimeField,FloatField,IntField
import datetime

class Category(Document):
    _id = StringField(primary_key=True,required=True)
    category = StringField(required=True)
    pant_size = IntField(required=False)
    pant_colour = StringField(required=False)
    pant_price = FloatField(required=False)
    shirt_size = IntField(required=False)
    shirt_colour = StringField(required=False)
    shirt_price = FloatField(required=False)
    image = StringField(required=False,default=None)
    product_id = StringField(required=True) 
    quantity = IntField(required=True) 
    vendor_owner_id = StringField(required=True) 
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    modified_at = DateTimeField(default=None)

  