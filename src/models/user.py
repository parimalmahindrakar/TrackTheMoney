from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
  username = StringField(required=True)
  email = EmailField(required=True)
  password = StringField(required=True)
  created_at = DateTimeField(default=datetime.utcnow)
  udpated_at = DateTimeField(default=datetime.utcnow)
