import os
from flask import Flask, request, abort, jsonify, render_template, Response, flash, redirect, url_for
from models import setup_db, Movie, Actor, db
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_cors import CORS

def create_app(test_config=None):
	# create and configure the app
	# app = Flask(__name__, template_folder='../frontend/templates')
	app = Flask(__name__)
	setup_db(app)
	CORS(app)
	# migrate = Migrate(app,db)

	@app.route('/')
	def index():
		return render_template('pages/home.html')

	# MOVIES
	@app.route('/movies')
	def movies():
		movies = Movie.query.all()
		# body = {
		# 	'id':actor.id,
		# 	'name': actor.name,
		# 	'gender':actor.gender,
		# 	'age':actor.age
		# }
		return render_template('pages/movies.html', movies=movies)

	@app.route('/movies/create', methods=['POST'])
	def post_movies():
		return

	# MOVIE
	@app.route('/movies/<int:movie_id>')
	def show_movie(movie_id):
		movie = Movie.query.get(movie_id)

		return render_template('pages/movie.html', movie=movie)

	@app.route('/movies/<int:movie_id>', methods=['PATCH'])
	def edit_movie(movie_id):
		return

	@app.route('/movies/<int:movie_id>', methods=['DELETE'])
	def delete_movie(movie_id):
		return

	# ACTORS
	@app.route('/actors')
	def actors():
		actors = Actor.query.all()
		# body = {
		# 	'id':actor.id,
		# 	'name': actor.name,
		# 	'gender':actor.gender,
		# 	'age':actor.age
		# }
		return render_template('pages/actors.html', actors=actors)

	@app.route('/actors/create', methods=['POST'])
	def post_actors():
		return
		
	# MOVIE
	@app.route('/actors/<int:actor_id>')
	def show_actor(actor_id):
		actor = Actor.query.get(actor_id)

		return render_template('pages/actor.html', actor=actor)

	@app.route('/actors/<int:actor_id>', methods=['PATCH'])
	def edit_actor(actor_id):
		return

	@app.route('/actors/<int:actor_id>', methods=['DELETE'])
	def delete_actor(actor_id):
		return


	return app

APP = create_app()

if __name__ == '__main__':
	APP.run(debug=True)
    # APP.run(host='0.0.0.0', port=8080, debug=True)