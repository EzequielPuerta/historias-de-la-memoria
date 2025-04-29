from enum import Enum
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    EmbeddedDocumentListField,
    StringField,
    ObjectIdField,
    EnumField,
)


class DataSourceEntry(EmbeddedDocument):
    data_source = StringField(required=True, null=False)
    url = StringField(required=True, null=False)


class Victim(EmbeddedDocument):
    name = StringField(required=True, null=False)
    _id = ObjectIdField()
    source_entry = EmbeddedDocumentField(DataSourceEntry, required=True, null=False)


class Relative(EmbeddedDocument):
    victim = EmbeddedDocumentField(Victim, required=True, null=False)
    relationship = StringField(required=True, null=False)


class PhotoType(Enum):
    PORTRAIT = "Retrato"
    DOCUMENT = "Documento"
    TRIBUTE = "Homenaje"
    TILE = "Baldoza"


class Photo(EmbeddedDocument):
    type = EnumField(PhotoType, required=True, null=False)
    url = StringField(required=True, null=False)


class RelatedVictim(Document):
    _id = ObjectIdField()
    name = StringField(required=True, null=False)
    source_entry = EmbeddedDocumentField(DataSourceEntry, required=True, null=False)
    photos = EmbeddedDocumentListField(Photo, required=False, null=False, default=[])
    related_victims = EmbeddedDocumentListField(Relative, required=True, null=False)
    related_victims_count = IntField(required=True, null=False)
    meta = {"collection": "related_victims"}
