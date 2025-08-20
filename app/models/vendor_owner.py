from mongoengine import Document, StringField, IntField, DateTimeField
import datetime

class Vendor_owner(Document):
    _id = StringField(primary_key=True,required=True)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobile = IntField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed password!
    onboarded_time = DateTimeField(default=datetime.datetime.utcnow)
    country_code = IntField(required=True)
    gender = StringField(required=True)
    brand_name = StringField(required=True)
    address = StringField(required=True)
    pincode = IntField(required=True)
    dob = StringField(required=False)
    modified_at = DateTimeField(default=None)
    store_address = StringField(required=False)
    gst = StringField(required=False)


