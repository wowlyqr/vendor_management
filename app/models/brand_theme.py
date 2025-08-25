from mongoengine import Document, StringField, DateTimeField
import datetime

class Brand_theme(Document):
    _id = StringField(primary_key=True,required=True)    
    theme_color = StringField(required=False,default=None) 
    brand_logo = StringField(required=False)     
    vendor_owner_id = StringField(required=True) 
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    modified_at = DateTimeField(default=None)

  