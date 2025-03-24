from mongoengine import Document, IntField, StringField, ObjectIdField


class MurdersAndKidnappings(Document):
    _id = ObjectIdField()
    count = IntField(required=True)
    fact_type = StringField(required=True)
