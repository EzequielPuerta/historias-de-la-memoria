from mongoengine import Document, IntField, FloatField, ObjectIdField


class PregnantsPerYear(Document):
    _id = ObjectIdField()
    total_count = IntField(required=True)
    pregnant_count = IntField(required=True)
    percentage_pregnant = FloatField(required=True)
    year = IntField(required=True)
