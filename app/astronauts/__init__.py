from flask import Blueprint
from flask_restful import Api

bp_astronauts = Blueprint('astronauts', __name__, template_folder='templates')
bp_astronauts_api = Api(bp_astronauts)

from . import routes
