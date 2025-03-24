from mongoengine import Document, IntField, ObjectIdField


class MixAndMaxAges(Document):
    _id = ObjectIdField()
    min_age = IntField(required=True)
    max_age = IntField(required=True)
    meta = {"collection": "min_and_max_ages"}
