from flask import Blueprint
from flask_restful import Api
from .views import ImagesRootView, ImagesView, ImagesWeakView, ImageView, ImageOuputView


processed_image_api_bp = Blueprint('api', __name__)
api = Api(processed_image_api_bp)


# Views
api.add_resource(ImagesRootView, '')
api.add_resource(ImagesView, 'images/')
api.add_resource(ImagesWeakView, 'images/weak/')
api.add_resource(ImageView, 'images/<id>/')
api.add_resource(ImageOuputView, 'images/<id>/output/')

'''
/images
GET - http://127.0.0.1:8000/api/images/
POST - http://127.0.0.1:8000/api/images/

GET - http://127.0.0.1:8000/api/images/weak/

/images/<id>
PUT - http://127.0.0.1:8000/api/images/<id>
GET - http://127.0.0.1:8000/api/images/<id>
DELETE - http://127.0.0.1:8000/api/images/<id>

/images/<id>/output
GET - http://127.0.0.1:8000/api/images/<id>/output
'''
