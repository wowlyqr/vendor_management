from mongoengine import Document, StringField, IntField, DateTimeField
import datetime

class Shop(Document):
    _id = StringField(primary_key=True,required=True)
    shop_name = StringField(required=True)
    shop_unique_id = StringField(required=True)
    address = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)
    vendor_owner_id = StringField(required=True)
    expected_open_date = StringField(required=False)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    modified_at = DateTimeField(default=None)

 