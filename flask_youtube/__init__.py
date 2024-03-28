from flask import Flask

def crate_app(config_file = 'settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    return app