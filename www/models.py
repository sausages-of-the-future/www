from mongoengine import StringField, DynamicDocument

class Service(DynamicDocument):
    slug = StringField(required=True)
    name = StringField(required=True)
