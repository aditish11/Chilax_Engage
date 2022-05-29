from flask import Flask

from app.routes.routes import blueprint
from app.auth.auth import auth_blueprint
from app.home.home import home_blueprint
from app.error.error import error_blueprint
from app.index.index import index_blueprint
from app.search.search import search_blueprint
from app.tunes.tunes import tunes_blueprint
from app.artist.artist import artist_blueprint

def create_app():
    """
    Creating and returning the app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'JUSTARANDOMKEY'

    app.register_blueprint(blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(artist_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(tunes_blueprint)
    return app
