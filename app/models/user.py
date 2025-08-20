from mongoengine import Document, StringField, ListField, IntField, DateTimeField
import datetime

class Users(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed password!
    roles = ListField(StringField(), default=list)  # e.g., ['admin', 'user']
    createdAt = DateTimeField(default=datetime.datetime.now)
    user_type = StringField(required=True)
    mobile = IntField(required=True)
    country_code = IntField(required=True)
