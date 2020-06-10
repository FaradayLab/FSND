import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor, db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	CORS(app)
	migrate = Migrate(app,db)
	
	@app.route('/')
	def home():
		actor = Actor.query.one()
		body = {
			'id':actor.id,
			'name': actor.name,
			'gender':actor.gender,
			'age':actor.age
		}

		return jsonify(body)

	return app

APP = create_app()

if __name__ == '__main__':
	APP.run(debug=True)
    # APP.run(host='0.0.0.0', port=8080, debug=True)