from mongoengine import StringField, DynamicDocument, BooleanField, ListField, DictField

class Service(DynamicDocument):

    slug = StringField(required=True)
    name = StringField(required=True)
    service_base_url_config = StringField()
    policies = ListField(StringField())
    legislation = ListField(DictField())
    registers = ListField(StringField())
    minister = StringField()

class Page(DynamicDocument):
    slug = StringField(required=True)
    page_type = StringField()
    title = StringField(required=True)
    markdown = StringField(required=True)
    json = StringField()



