from mongoengine import StringField, DynamicDocument, BooleanField, ListField, DictField

class Service(DynamicDocument):
    slug = StringField(required=True)
    name = StringField(required=True)
    policies = ListField(StringField())
    legislation = ListField(DictField())
