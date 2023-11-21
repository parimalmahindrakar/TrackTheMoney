from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    udpated_at = DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return User.objects(username=username).first()
