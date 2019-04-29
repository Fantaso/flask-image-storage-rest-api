from image_app import create_app

from flask_script import Manager, Server


app_env = 'development'
app = create_app(app_env)

manager = Manager(app=app)
manager.add_command('runserver', Server(host='0.0.0.0', port=8000))


if __name__ == '__main__':
    manager.run()
