import os
import json
import datetime
from flask import Flask

from flask_cors import CORS
#from flask_login import LoginManager, current_user, login_user, login_required, logout_user




from datetime import timedelta 
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS

from App.models import db, User

from App.views import (
    api_views,
    user_views
)

from App.login import login_manager






def get_db_uri(scheme='sqlite://', user='', password='', host='//demo.db', port='', name=''):
    return scheme+'://'+user+':'+password+'@'+host+':'+port+'/'+name 

def loadConfig(app):
    #try to load config from file, if fails then try to load from environment
    try:
        app.config.from_object('App.config')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if app.config['SQLITEDB'] else app.config['DBURI']
    except:
        print("config file not present using environment variables\n\n\n")
        # DBUSER = os.environ.get("DBUSER")
        # DBPASSWORD = os.environ.get("DBPASSWORD")
        # DBHOST = os.environ.get("DBHOST")
        # DBPORT = os.environ.get("DBPORT")
        # DBNAME = os.environ.get("DBNAME")
        DBURI = os.environ.get("DATABASE_URL")
        SQLITEDB = os.environ.get("SQLITEDB", default="true")
        app.config['ENV'] = os.environ.get("ENV")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if SQLITEDB in {'True', 'true', 'TRUE'} else DBURI

def create_app():
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    return app

  
 



app = create_app()

app.app_context().push()

app.register_blueprint(api_views)
app.register_blueprint(user_views)

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''
