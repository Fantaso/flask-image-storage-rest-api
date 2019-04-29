from mongoengine import Document, EmbeddedDocument
from mongoengine import fields


class ImageOutputDocument(EmbeddedDocument):
    probability = fields.FloatField(required=True)
    label = fields.StringField(required=True)
    result = fields.StringField(required=True)
    bbox = fields.ListField(fields.FloatField(required=True))

    meta = {
        'db_alias': 'main',
        'collection': 'imageoutputs',
    }

    def __str__(self):
        return f'<output: {self.probability} {self.label} {self.result}>'


class ImageDocument(Document):
    COMPLETE = 'complete'
    PROCESSING = 'processing'
    STATUS_CHOICES = (COMPLETE, PROCESSING)

    status = fields.StringField(required=True, choices=STATUS_CHOICES)
    imagePath = fields.StringField(required=True)
    imageId = fields.StringField(required=True)
    output = fields.EmbeddedDocumentListField(ImageOutputDocument)
    weak = fields.BooleanField(default=False)

    meta = {
        'db_alias': 'main',
        'collection': 'images',
    }

    def __str__(self):
        return f'<imageId: {self.imageId}>'
