from mongoengine import Document, IntField, ObjectIdField


class MilitancyByMonthAndYear(Document):
    _id = ObjectIdField()
    year = IntField(required=True)
    month = IntField(required=True)
    with_militancy = IntField(required=False)
    without_militancy = IntField(required=False)
