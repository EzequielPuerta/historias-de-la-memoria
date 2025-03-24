from mongoengine import Document, IntField, ObjectIdField


class MurdersAndKidnappingsByMonthAndYear(Document):
    _id = ObjectIdField()
    murders_count = IntField(required=True)
    kidnappings_count = IntField(required=True)
    year = IntField(required=True)
    month = IntField(required=True)
