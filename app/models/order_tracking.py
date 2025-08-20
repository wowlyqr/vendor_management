from mongoengine import Document, StringField, DateTimeField
import datetime

class Order_Tracking(Document):
    _id = StringField(primary_key=True,required=True)
    order_id = StringField(required=True)
    status = StringField(required=True)
    description = StringField(required=False)    
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    