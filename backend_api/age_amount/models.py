from mongoengine import Document, IntField, ObjectIdField


class AgeAmount(Document):
    _id = ObjectIdField()
    _from = IntField(required=True)
    _to = IntField(required=True)
    count = IntField(required=True)
    meta = {"collection": "age_amount"}
