from mongoengine import StringField, DateTimeField, DictField, PolygonField, PointField, Document, BooleanField, URLField

class  Service(DynamicDocument):
    slug = StringField(required=True)
    name = StringField(required=True)
