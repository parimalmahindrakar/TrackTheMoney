from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, ListField, LazyReferenceField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username    = StringField(required=True, max_length=20)
    first_name  = StringField(required=True, max_length=30)
    last_name   = StringField(required=True, max_length=30)
    email       = EmailField(required=True, max_length=50)
    password    = StringField(required=True)
    is_admin    = BooleanField(default=False)
    banks       = ListField(LazyReferenceField("Bank"))
    created_at  = DateTimeField(default=datetime.utcnow)
    udpated_at  = DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return User.objects(username=username).first()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
