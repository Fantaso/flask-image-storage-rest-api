from flask import request
from flask_restful import Resource
from marshmallow import ValidationError, pprint

from .models import ImageOutputDocument, ImageDocument
from .serializers import ImageOutputSerializer, ImageSerializer


class ImagesRootView(Resource):
    # List
    def get(self):
        """
        Get all images stored in Images Storage REST API.
        """
        return {'message': 'You are in the Image API Root view. Try /images/'}, 200

##########################################
######## Images List Create           ####
########        GET  POST             ####
########    /images/                  ####


class ImagesView(Resource):
    # List
    def get(self):
        """
        Get all images stored in Images Storage REST API.
        """

        # get all images from database
        # deserialize all images database objects to serializable data
        # send the result with 200 OK HTTP
        images = ImageDocument.objects.all()
        result = ImageSerializer(many=True, exclude=('weak',)).dump(images).data
        return result, 200

    # Create
    def post(self):
        """
        Create an image stored in Images Storage REST API.
        """

        # get request data
        json_request = request.get_json()

        # Custom validation
        try:
            result = ImageSerializer().load(json_request)
        except ValidationError as err:
            return err.messages, 400

        # In built validation (e.g required)
        if result.errors:
            return result.errors, 400

        # dump the result to get the weak method field to work
        # get the nested "output" field
        # create the imagedocument without the "output"
        # create the imageoutputdocument
        # attach the imageoutputdocument to the nested imagedocument field "output"
        # save and commit the database
        dump_result = ImageSerializer().dump(result.data).data
        output = dump_result.pop('output')[0]
        image = ImageDocument(**dump_result).save()
        image_output = ImageOutputDocument(**output)
        image.output.append(image_output)
        image.save()

        # retrieve image created and serialize it to send it back
        obj_image = ImageDocument.objects(id=image.id).first()
        ser_image = ImageSerializer(exclude=('weak',)).dump(obj_image)

        return ser_image.data, 202

# errors = UserSchema().validate({'name': 'Ronnie', 'email': 'invalid-email'})
# errors  # {'email': ['"invalid-email" is not a valid email address.']}

##########################################
######## Image Retrieve Update Delete ####
########       GET      PUT    DELETE ####
########    /images/<id>/             ####


class ImageView(Resource):
    # Retrieve
    def get(self, id):
        """
        Get an image details stored in Images Storage REST API.
        """

        # get an images from database
        # check if that image exist
        # deserialize the images database objects to serializable data
        # send the result with 200 OK HTTP
        image = ImageDocument.objects.filter(imageId=str(id))
        if not image:
            return {'error': f'imageId: {id} does not exist!'}, 400

        result = ImageSerializer(exclude=('weak',)).dump(image.first()).data
        return result, 200

    # Update

    def put(self, id):

        # retreive image from database
        image = ImageDocument.objects(imageId=str(id))
        if not image:
            return {'error': f'imageId: {id} does not exist!'}, 400

        # get request data
        json_request = request.get_json()

        # Custom validation
        try:
            result = ImageSerializer().load(json_request)
        except ValidationError as err:
            print(err)
            return {'errors': err.messages, 'msg': err}, 400

        # In built validation (e.g required)
        if result.errors:
            return result.errors, 400

        # dump the result to get the weak method field to work
        dump_result = ImageSerializer().dump(result.data).data

        # retreive the lazy query and update the image
        image = image.first()
        image.update(**dump_result)

        # retrieve image created and serialize it to send it back
        obj_image = ImageDocument.objects(id=image.id).first()
        ser_image = ImageSerializer(exclude=('weak',)).dump(obj_image)

        return ser_image.data, 200

    # Delete

    def delete(self, id):
        """
        Delete an image stored in Images Storage REST API.
        """

        # get an images from database
        # check if that image exist
        # delete the image from database
        # send the result with 204 HTTP NO CONTENT
        image = ImageDocument.objects(imageId=str(id))
        if not image:
            return {'error': f'imageId: {id} does not exist!'}, 400

        image.first().delete()
        return {'message': 'Deleted successfully!'}, 204


##########################################
######## ImageOutput Retrieve         ####
########             GET              ####
########    /images/<id>/output/      ####
class ImageOuputView(Resource):
    # Retrieve
    def get(self, id):
        """
        Get an image output details stored in Images Storage REST API.
        """

        # get an image from database
        # check if that image exist
        # deserialize the output's image database object to serializable data
        # send the result with 200 OK HTTP
        image = ImageDocument.objects.filter(imageId=str(id))
        if not image:
            return {'error': f'imageId: {id} does not exist!'}, 400

        result = ImageSerializer().dump(image.first()).data.pop('output')[0]
        return result, 200

##########################################
######## ImagesWeak  Retrieve         ####
########             GET              ####
########    /images/<id>/weak/        ####


class ImagesWeakView(Resource):
    # Retrieve
    def get(self):
        """
        Get all weak image list stored in Images Storage REST API.
        """

        # get all images from database
        # check if that image exist
        # deserialize the images database objects to serializable data
        # send the result with 200 OK HTTP
        images = ImageDocument.objects.filter(weak=True)
        if not images:
            return {'message': 'Hooray! No weak images found.'}, 200

        result = ImageSerializer(many=True, exclude=('weak',)).dump(images).data
        return result, 200
