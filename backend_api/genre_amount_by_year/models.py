from mongoengine import Document, IntField, ObjectIdField


class GenreAmountByYear(Document):
    _id = ObjectIdField()
    year = IntField(required=True)
    male_count = IntField(required=True)
    female_count = IntField(required=True)
