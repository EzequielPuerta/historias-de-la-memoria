from mongoengine import Document, IntField, StringField, ObjectIdField


class NationalitiesAmount(Document):
    _id = ObjectIdField()
    count = IntField(required=True)
    nationality = StringField(required=True)
