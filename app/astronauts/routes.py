import io
import math
from flask import Blueprint, render_template, send_file, jsonify, request, render_template_string, redirect
from flask import current_app as app
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc

from pprint import pprint
from app import db
from . import bp_astronauts_api, bp_astronauts
from .models import Astronaut

# @bp_astronauts.route("/test")
# def test():
#     return render_template_string("url_is {{url_for('static', filename='index.html')}}")

@bp_astronauts.route("/")
def main():
    return redirect("/index.html")

parser_astronaut = reqparse.RequestParser(bundle_errors=True)
parser_astronaut.add_argument('firstName', type=str, required=True, help="firstName is required parameter!")
parser_astronaut.add_argument('lastName', type=str, required=True, help="lastName is required parameter!")
parser_astronaut.add_argument('dateOfBirth', type=str, required=True, help="superpower is required parameter!")
parser_astronaut.add_argument('superpower', type=str, required=True, help="superpower is required parameter!")
parser_astronaut.add_argument('order', type=str, required=False, help="order is not required parameter!")
parser_astronaut.add_argument('orderBy', type=str, required=False, help="orderBy is not required parameter!")
parser_astronaut.add_argument('page', type=str, required=False, help="page is not required parameter!")
parser_astronaut.add_argument('rowsPerPage', type=str, required=False, help="rowsPerPage is not required parameter!")

def check_condition(string_to_check): 
        return string_to_check == None or string_to_check == ""

class astronauts(Resource):
    def get(self):  
        print(request.args)      
        orderBy = request.args.get('  orderBy', default = "id", type = str)                  
        order = request.args.get('  order', default = "asc", type = str)               
        page = request.args.get('  page', default = 1, type = int)                       
        rowsPerPage = request.args.get('  rowsPerPage', default = 5, type = int)
        firstName = request.args.get('  firstName', default = "", type=str)                           
        lastName = request.args.get('  lastName', default = "", type=str)           
        dateOfBirth = request.args.get('  dateOfBirth', default = "", type=str)  
        superpower = request.args.get('  superpower', default = "", type=str)    

        astronauts = Astronaut.query \
            .filter(Astronaut.firstName.contains(firstName)) \
            .filter(Astronaut.lastName.contains(lastName)) \
            .filter(Astronaut.dateOfBirth.contains(dateOfBirth)) \
            .filter(Astronaut.superpower.contains(superpower)) \
            .order_by(asc(orderBy) if (order == "asc") else desc(orderBy)) \
            .all()

        filtered_astronauts_length = len(astronauts)
        last_page = math.ceil(filtered_astronauts_length / rowsPerPage)
        astronauts_paginated = astronauts[(page - 1)*rowsPerPage: (page - 1) * rowsPerPage + rowsPerPage]
        return {"total": filtered_astronauts_length, "page": page, "lastPage": last_page, "rowsPerPage": rowsPerPage, "astronauts": [Astronaut.serialize(astronaut) for astronaut in astronauts_paginated]}

    def post(self):
        args_astronaut = parser_astronaut.parse_args()
        print(args_astronaut)
     
        astronaut = Astronaut(firstName=args_astronaut['firstName'], 
                      lastName=args_astronaut['lastName'], 
                      dateOfBirth=args_astronaut['dateOfBirth'],
                      superpower=args_astronaut['superpower'])
        print(astronaut)
        try:                
            db.session.add(astronaut) 
            db.session.commit()     
            return Astronaut.serialize(astronaut), 201
        except IntegrityError:
            db.session.rollback()
            return {"error":"Can't add astronaut to db"} , 400
        
            
    
class astronaut(Resource):
    def get(self, astronaut_id):
        return Astronaut.serialize(
                Astronaut.query.filter_by(id=astronaut_id)
                .first_or_404(description='Astronaut with id={} is not available'.format(astronaut_id)))
    
    def delete(self, astronaut_id):
        astronaut = Astronaut.query.filter_by(id=astronaut_id).first_or_404(description='Astronaut with id={} is not available'.format(astronaut_id))
        try:                
            db.session.delete(astronaut) 
            db.session.commit()     
            return Astronaut.serialize(astronaut), 200
        except IntegrityError:
            db.session.rollback()
            return {"error":"Can't remove astronaut from db"} , 400
    
    def put(self, astronaut_id):
        args_astronaut = parser_astronaut.parse_args()

        astronaut = Astronaut.query.filter_by(id=astronaut_id).first_or_404(description='Astronaut with id={} is not available'.format(astronaut_id))
        astronaut.firstName=args_astronaut['firstName']
        astronaut.lastName=args_astronaut['lastName']
        astronaut.dateOfBirth=args_astronaut['dateOfBirth']
        astronaut.superpower=args_astronaut['superpower']
        
        try:                
            db.session.add(astronaut) 
            db.session.commit()     
            return Astronaut.serialize(astronaut), 200
        except IntegrityError:
            db.session.rollback()
            return {"error":"can't add astronaut to db"} , 400

bp_astronauts_api.add_resource(astronauts, '/api/astronauts','/')
bp_astronauts_api.add_resource(astronaut, '/api/astronauts/<astronaut_id>','/')
