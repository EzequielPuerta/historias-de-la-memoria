from mongoengine import Document, StringField, IntField, ObjectIdField


class GenreAmount(Document):
    _id = ObjectIdField()
    count = IntField(required=True)
    genre = StringField(required=False)
