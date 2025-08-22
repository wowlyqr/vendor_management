from mongoengine import Document, StringField, IntField, DateTimeField
import datetime

class Admin(Document):
    _id = StringField(primary_key=True,required=True)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobile = IntField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed password!
    onboarded_time = DateTimeField(default=datetime.datetime.utcnow)
    country_code = IntField(required=True)
    gender = StringField(required=True)   
