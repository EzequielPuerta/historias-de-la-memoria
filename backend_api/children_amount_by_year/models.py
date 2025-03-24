from mongoengine import Document, IntField, ObjectIdField


class ChildrenAmountByYear(Document):
    _id = ObjectIdField()
    total_children = IntField(required=True)
    year = IntField(required=True)
