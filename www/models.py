from mongoengine import StringField, DynamicDocument, BooleanField, ListField, DictField

from flask.ext.security import UserMixin, RoleMixin

from www import db

class Service(DynamicDocument):
    slug = StringField(required=True)
    name = StringField(required=True)
    description = StringField()
    service_base_url_config = StringField()
    policies = ListField(StringField())
    legislation = ListField(DictField())
    stats = ListField(DictField())
    registers = ListField(StringField())
    minister = StringField()

class Page(DynamicDocument):
    slug = StringField(required=True)
    page_type = StringField()
    title = StringField(required=True)
    markdown = StringField(required=True)
    json = StringField()

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])

class InviteApplicant(db.Document):
    full_name = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    email_confirmed = db.BooleanField(default=False)
    invited = db.BooleanField(default=False)


