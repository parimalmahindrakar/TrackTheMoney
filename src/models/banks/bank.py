from mongoengine import Document, StringField, LazyReferenceField, FloatField, DENY

class Bank(Document):
    name                    = StringField(required=True)
    total_initial_amount    = FloatField(required=True)
    total_remaining_amount  = FloatField(required=True)
    user                    = LazyReferenceField('User', reverse_delete_rule=DENY)

    def __repr__(self):
        return f'<Bank:{self.name}>'

    def get_user(self):
        return self.user.fetch()
