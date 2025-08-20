from mongoengine import Document, StringField, IntField, DateTimeField,BooleanField
import datetime

class Credentials(Document):
    _id = StringField(primary_key=True,required=True)
    user_id = StringField(required=True)
    user_type = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobile = IntField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed password!
    update_password = BooleanField(default=False)  
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    country_code = IntField(required=True)
    

