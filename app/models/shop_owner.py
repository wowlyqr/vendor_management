from mongoengine import Document, StringField, IntField, DateTimeField
import datetime

class Shop_owner(Document):
    _id = StringField(primary_key=True,required=True)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobile = IntField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed password!
    onboarded_time = DateTimeField(default=datetime.datetime.utcnow)
    country_code = IntField(required=True)
    aadhar_number = StringField(required=False,default=None)
    gender = StringField(required=True)    
    shop_id = StringField(required=True)    
    vendor_id = StringField(required=True)
    modified_at = DateTimeField(default=None)