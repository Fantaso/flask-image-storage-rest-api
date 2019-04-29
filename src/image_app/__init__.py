from flask import Flask, jsonify


from image_app.config import APP_CONFIG, db_connect


def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[app_env])

    db_connect(app_env)

    from image_app.processed_image_api import processed_image_api_bp
    app.register_blueprint(processed_image_api_bp, url_prefix='/api/')

    @app.route('/')
    def index():
        """You are at Index Processed Image Storage REST API."""
        return jsonify({'message': 'You are @ Index Processed Image Storage REST API. Visit /api/'})

    return app
