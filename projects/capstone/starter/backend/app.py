import os
from flask import Flask, request, abort, jsonify
from models import setup_db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	# setup_db(app)
	# CORS(app)

	@app.route('/')
	def home():
		greeting = 'Hello, World!' 
		return greeting

	return app

APP = create_app()

if __name__ == '__main__':
	APP.run(debug=True)
    # APP.run(host='0.0.0.0', port=8080, debug=True)