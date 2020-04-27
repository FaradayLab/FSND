import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    drinks_short = [drink.short() for drink in drinks]

    return jsonify({'success': True, 'drinks': drinks_short})


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    drinks_long = [drink.long() for drink in drinks]

    return jsonify({'success': True, 'drinks': drinks_long})


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    print('it does come in here')
    body = request.get_json()
    title = body.get('title', None)
    recipe = json.dumps(body.get('recipe', None))

    if not title or not recipe:
        abort(422)
    
    drink = Drink.query.filter(Drink.title==title).one_or_none()
    if drink:
        abort(409)

    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
    except Exception:
        abort(422)

    return jsonify({'success': True, 'drinks': [drink.long()]})


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload,drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one()
    if not drink:
        abort(400)

    body = request.get_json()
    title = body.get('title', None)
    recipe = json.dumps(body.get('recipe', None))

    try:
        drink.title = title
        drink.recipe = recipe
        drink.update()
    except Exception as identifier:
        abort(422)

    return jsonify({'success': True, 'drinks': [drink.long()]})


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload,drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    if not drink:
        abort(400)

    try:
        drink.delete()
    except Exception as identifier:
        abort(422)
        
    return jsonify({'success': True, 'delete': drink_id})


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422
        
@app.errorhandler(409)
def conflict(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "conflicts with some rule already established"
    }), 409

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authorize_authenticate_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code