from marshmallow import Schema, ValidationError, fields, pprint, validates

from .models import ImageDocument, ImageOutputDocument


class ImageOutputSerializer(Schema):
    probability = fields.Float(allow_nan=False,  required=False)
    label = fields.String(required=True)
    result = fields.String(required=True)
    bbox = fields.List(fields.Float(allow_nan=False),  required=False)

    class Meta:
        fields = ("probability", "label", "result", "bbox")
        ordered = True


class ImageSerializer(Schema):
    COMPLETE = 'complete'
    PROCESSING = 'processing'
    STATUS_CHOICES = (COMPLETE, PROCESSING)

    status = fields.String(required=True, error_messages={'required': 'Status is required.'})
    imagePath = fields.String(required=True)
    imageId = fields.String(required=True)
    output = fields.Nested(ImageOutputSerializer, many=True, required=True)
    weak = fields.Method('get_weak', dump_only=True)

    class Meta:
        fields = ('status', 'imagePath', 'imageId', 'output', 'weak')
        ordered = True

    def get_weak(self, obj):
        if obj['output'][0]['probability'] > 0.7:
            return False
        elif obj['output'][0]['probability'] <= 0.7:
            return True
        else:
            return None

    @validates('status')
    def validate_status(self, value):
        if value != ImageSerializer.COMPLETE and value != ImageSerializer.PROCESSING:
            raise ValidationError(
                f"'{value}' Must be '{ImageSerializer.COMPLETE}' or '{ImageSerializer.PROCESSING}'")

    # @validates('imageId')
    # def validate_imageId(self, value):
    #     image = ImageDocument.objects(imageId=value)
    #     if image:
    #         raise ValidationError(f"imageId: {value} already exists!")
