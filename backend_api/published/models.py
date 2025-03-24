from mongoengine import Document, IntField, ListField, StringField, ObjectIdField


class Published(Document):
    _id = ObjectIdField()
    day = IntField(required=True)
    month = IntField(required=True)
    desaparecidos = ListField(StringField(), required=True)
