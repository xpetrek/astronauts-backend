import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
from flask_restful import Resource, Api, abort, reqparse

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()
# app = Flask(__name__, static_folder='static', static_url_path='')

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    CORS(app) 

    ###### configs ########
    # app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql-dimensional-76949'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.config['SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnm'
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    ###### init extensions ########
    db.init_app(app)
    ma.init_app(app)
    # cors.init_app(app, resources={r"/astronauts": {"origins": "*"}})

    ###### blueprints registrations ########
    from app.astronauts import bp_astronauts as astronauts_blueprint
    app.register_blueprint(astronauts_blueprint)
    # from app.frontend import bp_frontend as frontend_blueprint
    # app.register_blueprint(frontend_blueprint)    
    db.create_all()
    
    return app
