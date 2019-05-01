<!-- logo -->
<a href="https://www.fantaso.de">
<img src="/readme/fantaso.png" align="right" />
</a>

<!-- header -->
<h1 style="text-align: left; margin-top:0px;">
  Processed Image REST API
</h1>

> Rest Api app done with Flask and flask_restful.

<!-- build -->
<!-- [![Build Status][travis-image]][travis-link] -->




Project consists to allow a embedded system to store a processed image ouput through at a external system and have that data available through a REST Api. This Api has been manually tested but there won't be any automated tests as this was developed as showcase only.



How Processed Image Api Works:
- You send a HTTP POST request to the `/api/images/` endpoint with the `Document Image File` to be stored in Json format. A `Document Image file` looks like:
            {
                "status":"complete" or "processing",
                "imagePath":"date/image_name.jpg",
                "imageId":"image_id",
                "output":[
                    {
                        "bbox":[
                            10.11,
                            20.22,
                            30.33,
                            40.44
                        ],
                        "probability":0.95,
                        "label":"object_in_image_name",
                        "result":"verbose_name_of_probability"
                    }
                ]
            }

- You send a HTTP GET request to retrieve a list of all images stored in the database at `/api/images/`.
- Alternatively there are more endpoints to interact with the REST Api. See more below.

<br><br>

## Index:
- #### Installation
    1. Installing Flask Processed Image REST API

- #### Usage:
    1. Access and Used Flask Processed Image REST API with Po
    2. Available Endpoints

- #### Information:
- #### Maintainer


<br><br>


## Installation:
#### 1.Installing Flask API App Using ![docker-compose][docker-compose]:


1. Clone repository and go inside the repository folder "flask-image-storage-rest-api"
```sh
git clone https://github.com/Fantaso/flask-image-storage-rest-api.git
```

2. Before you run the Api, you must configure a Mongo database. You can use one for free at Mongodb website with a free tier with the Mongo Atlas service. Once that you can need to copy the mongodb URI endpoint to connect the Api with the database. the mongodb URI from MongoDB Atlas would like this:
```sh
mongodb+srv://username:password@cluster-name.mongodb.net/test?retryWrites=true
```

3. Copy the database URI to the `MONGODB_HOST` configuration at `flask-image-storage-rest-api/src/image_app/config.py`. Replace all or the one you will use. Incase you want change which environment the app uses to determine which database will use you have modify it here `flask-image-storage-rest-api/src/manage.py` where `app_env='development'` is used.
```python
MONGODB_HOST = {
    'development': 'mongodb+srv://username:password@cluster-name.mongodb.net/test?retryWrites=true',
    'production': os.environ.get('MONGODB_HOST'),
    'testing': os.environ.get('MONGODB_HOST'),
}
```

4. Build the docker image and run docker container with docker-compose package. No need for migrating any database a we are using MongoDB.  
```sh
docker-compose up
```


<br>

## 2. Access and Used Flask Processed Image REST API

<!-- <br><br> -->


## Usage:
Once docker-compose is done downloading all images and none of the services failed after you have run the containers with `docker-compose up`

<br>

#### 1. Access and Interact with API Front-end app (django restframework)

You can access to see if the api is working from your web browser with url _http://0.0.0.0:8000/api/_

Alternatively, to interact and start using the API, you will need a tool send HTTP requests to your api. I have develop a list of request to test and interact with the api with Postman, which is a free software you could use. You will need to download the Postman Desktop app or the Web Browser plug in for Chrome. Click on the button below to guide you to download the app with the list of request I have developed to test the api fast.

[![Run in Postman][postman-button-svg]][postman-button-link]

If you already have the Postman app, you can also download the postman json file exported from the Postman app, which contains the configuration for the collection of requests and just import the configuration file (postman json file) into the app and you are ready to start using the api.

[Flask-image-storage-rest-api.postman_collection.json][postman-collection-file]


<br>

#### 2. Available Endpoints

Endpoints are categorized by the database's model architecture. The database choosen is MongoDB. The models for this API has an ImageDocument and a nested/embedded document called ImageOutputDocument:

1. ImageDocument model
  - `imagePath`:
  - `status`: The status of the image process stage. It is a Choices type of field, where you where you have either "complete" or "processing" as a String.
  - `imageId`: A string field containing the id serial or number for the specific image being processed.
  - `output`: Contains the results of the image being processed. It is a nested/relationship field that reference the ImageOutputDocument.
  - `weak`: This is a field used for only the API internal usage when querying a list of all images that are weak. This field is not part of the json file of the image nor is required when interacting with the API. This field it is used to determine if the results of the image processed has a weak or poor certainty based on the probability of certainty that the results are trust worthy or not. This field is automatically filled by the API when creating or adding a new image to the database. The rules to determine whether an image has a weak output or not is:
      - if the image output has a probability lower than 0.7 (70%) is considered a weak or not trust worthy analysis.
      - if the image output probability is higher that 0.7 (70%) is not considered a weak image.


2. ImageOutputDocument model
  - `probability`: The percentage result of the analisys of the image, which determines if the analysis of the image is trusted or not. It is given as a float number with a reprensatation range between 0 and 1 which means 0% or 100% of cerntainty.
  - `label`: The name of the object found in the image that is being processed.
  - `result`: A verbose name that represents the result of the probability of the image analysis as a string field
  - `bbox`: A list of float numbers which contains the points of the image pixels where the analysis and quality control has detected a possible problem.


<br>


###### Endpoint List
URI Example: `http://0.0.0.0:8000/api/images/<id>/`


| | Available Methods | URI |
| -: | :- | :- |
| | | |
| | **Image Endpoints** | |
| 1. | `GET` `POST`                      | `api/images/` |
| 2. | `GET` `PUT` `DELETE`              | `api/images/<id>/` |
| 3. | `GET`                             | `api/images/weak/` |
| 4. | `GET`                             | `api/images/<id>/output/` |


<br>

There are two models, however how we store or update a image json file is only through the ImageDocument serializer, which takes care of also creating the database object for the ImageOutputDocument and nested together. The api follow the REST standard with an extra method to have a CRUDL endpoints (Create, Retrieve, Update, Delete and List) and 2 more custom endpoints (6 and 7 in the table below).

Let's take **images endpoints** as an example:


| | Method | URI | Description |
| -: | :- | :- | :- |
| | URI Example:             |  `http://0.0.0.0:8000/api/images/<id>/` | |
| | | |
| 1. | `GET`                | `api/images/`            | Get a **List** of all image documents available |   
| 2. | `POST`               | `api/images/`            | **Create** an image document |    
| 3. | `GET`                | `api/images/<id>/`       | **Retrieve** an specific image with the imageId of the image document in the uri <id> section e.g. `api/images/2/`|    
| 4. | `PUT`                | `api/images/<id>/`       | **Update** an specific image |    
| 5. | `DELETE`             | `api/images/<id>/`       | **Delete** an specific image |
| | | |
| 6. | `GET`                | `api/images/weak/`       | Get a **List** of all image documents available which have a probability lower than 0.7 (70%) |
| 7. | `GET`                | `api/images/<id>/output` | Get the image output or result's details only of an specific ImageDocument which would be the ImageOutputDocument with the imageId in the uri <id>  section e.g `api/images/2/output` |

<br>



## Information:
| Technology Stack |  |  |
| :- | :-: | :- |
| Python                    | ![back-end][python]                     | Back-End |
| Flask                     | ![flask][flask]                         | Web Framework |
| Flask RESTful             | ![api-extension][flaskrestful]          | Flask API Extension |
| Marshmallow               | ![serializer][marshmallow]              | Serializer |
| Mongo DB                  | ![database][mongodb]                    | Database |
| Mongo Engine              | ![database-odm][mongoengine]            | ODM |
| Docker                    | ![container][docker]                    | Container |
| Docker-Compose            | ![container-manager][docker-compose]    | Container Manager |
| Postman                   | ![api-requests-app][postman]            | API Requests App |


<br><br>


## Maintainer
Get in touch -–> [fantaso.de][fantaso]



<!-- Links -->
<!-- Profiles -->
[github-profile]: https://github.com/fantaso/
[linkedin-profile]: https://www.linkedin.com/
[fantaso]: https://www.fantaso.de/
<!-- Extra -->
[postman-collection-file]: Flask-image-storage-rest-api.postman_collection.json
[postman-button-svg]:https://run.pstmn.io/button.svg
[postman-button-link]:https://app.getpostman.com/run-collection/f168ada6c6fcb51d3800

<!-- Repos -->
[github-repo]: https://github.com/Fantaso/flask-image-storage-rest-api

<!-- Builds -->
[travis-link]: https://travis-ci.org/
[travis-image]: https://travis-ci.org/

<!-- images -->
[python]: readme/python.png
[flask]: readme/flask.png
[flaskrestful]: readme/flaskrestful.png
[marshmallow]: readme/marshmallow.png
[mongodb]: readme/mongodb.png
[mongoengine]: readme/mongoengine.png
[docker]: readme/docker.png
[docker-compose]: readme/docker-compose.png
[postman]: readme/postman.png
