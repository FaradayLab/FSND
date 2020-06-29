import os
import dateutil.parser
import babel
from flask import Flask, request, abort, jsonify, render_template, Response, flash, redirect, url_for
from models import setup_db, Movie, Actor, db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf import Form
from forms import *
import sys

def create_app(test_config=None):
	# create and configure the app
	# app = Flask(__name__, template_folder='../frontend/templates')
	app = Flask(__name__)
	app.config.from_object('config')
	setup_db(app)
	CORS(app)
	migrate = Migrate(app,db)

	# ------------------------------------------------------------------------#
	# Filters
	# ------------------------------------------------------------------------#
	def format_datetime(value, format='medium'):
		date = dateutil.parser.parse(value)
		# if format == 'full':
		# 	format = "EEEE MMMM, d, y 'at' h:mma"
		# elif format == 'medium':
		# 	format = "EE MM-dd-y"
		return babel.dates.format_datetime(date, "EE MM-dd-y")

	app.jinja_env.filters['datetime'] = format_datetime

	# ------------------------------------------------------------------------#
	# Routes
	# ------------------------------------------------------------------------#

	@app.route('/')
	def index():
		return render_template('pages/home.html')

	# MOVIES
	@app.route('/movies')
	def movies():
		movies = Movie.query.all()
		return render_template('pages/movies.html', movies=movies)

	@app.route('/movies/create', methods=['GET'])
	def create_movie_form():
		form = MovieForm()
		return render_template('forms/new_movie.html', form=form)


	@app.route('/movies/create', methods=['POST'])
	def create_movie_submit():
		error = False
		form = MovieForm()
		if form.validate_on_submit():
			try:
				movie = Movie(
					title=form.title.data,
					release=form.release.data,
					image_link=form.image_link.data,
					# website=form.website.data,
					# facebook_link=form.facebook_link.data,
				)
				movie.insert()
			except:
				error = True
				print(sys.exc_info())
				movie.rollback()
			finally:
				movie.close()
				if error:
					flash(
						'An error occurred. Movie '
						+ request.form['title']
						+ ' could not be listed.'
					)
				else:
					flash('Movie ' + request.form['title'] + ' was successfully listed!')
		else:
			flash('One or more fields are not valid.')
			# flash(actor.facebook_link.data + ': ' + str(actor.errors['facebook_link']))
			return render_template('forms/new_movie.html', form=form)

		return redirect(url_for('movies'))
	# MOVIE
	@app.route('/movies/<int:movie_id>')
	def show_movie(movie_id):
		movie = Movie.query.get(movie_id)

		return render_template('pages/show_movie.html', movie=movie)

	@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
	def edit_movie(movie_id):
		print('GET GET')
		movie = Movie.query.get(movie_id)
		form = MovieForm(obj=movie)

		return render_template('forms/new_movie.html', form=form, movie=movie)

	@app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
	def edit_movie_submit(movie_id):
		# movie = Movie.query.get(movie_id)
		movie = Movie.query.filter(Movie.id==movie_id).one()
		form = MovieForm()
		error = False

		if form.validate_on_submit():
			try:
				movie.title = form.title.data
				movie.release = form.release.data
				movie.image_link = form.image_link.data

				movie.update()
				print('TRY')
			except:
				error = True
				print(sys.exc_info())
				movie.rollback()
			finally:
				# movie.close()
				print('FINALLY')
				if error:
					flash(
					'An error occurred. Movie '+'name'+' could not be added.'
					)
				else:
					print('NO ERROR')
					flash('Movie ' + 'name' + ' was successfully added!')
		else:
			print('ERROR')
			flash('One or more fields are not valid.')
			# flash(form.errors)
			return render_template('forms/new_movie.html', form=form, movie=movie)

		# return redirect(url_for('movies'))
		# return redirect(url_for('show_movie', movie_id=movie_id, _method='GET'))
		return render_template('pages/show_movie.html', movie=movie)
		# return redirect(url_for('index'))

	@app.route('/movies/<int:movie_id>', methods=['DELETE'])
	def delete_movie(movie_id):
		error = False
		movie = Movie.query.get(movie_id)
		movie_title = movie.title

		try:
			db.session.delete(movie)
			db.session.commit()
		except:
			error = True
			db.session.rollback()
		finally:
			db.session.close()

		if error:
			flash('An Error Occured')
		else:
			flash('Movie ' + movie_title + ' was successfully deleted!')

		return redirect(url_for('index'))

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

	@app.route('/actors/create', methods=['GET'])
	def create_actor_form():
		form = ActorForm()
		return render_template('forms/new_actor.html', form=form)


	@app.route('/actors/create', methods=['POST'])
	def create_actor_submit():
		error = False
		form = ActorForm()

		if form.validate_on_submit():
			try:
				actor = Actor(
					name=form.name.data,
					age=form.age.data,
					gender=form.gender.data,
					image_link=form.image_link.data,
					# website=actor.website.data,
					# facebook_link=actor.facebook_link.data,
				)
				actor.insert()
			except:
				error = True
				print(sys.exc_info())
				actor.rollback()
			finally:
				actor.close()
				if error:
					flash(
						'Error. Actor '+request.form['name']+' was not added.'
					)
				else:
					flash('Actor '+request.form['name']+' was added!')
		else:
			flash('One or more fields are not valid.')
			# flash(actor.facebook_link.data + ': ' + str(actor.errors['facebook_link']))
			return render_template('forms/new_actor.html', form=form)
		
		return redirect(url_for('actors'))
	# ACTOR
	@app.route('/actors/<int:actor_id>')
	def show_actor(actor_id):
		actor = Actor.query.get(actor_id)

		return render_template('pages/show_actor.html', actor=actor)

	@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
	def edit_actor(actor_id):
		print('GET GET')
		actor = Actor.query.get(actor_id)
		form = ActorForm(obj=actor)

		return render_template('forms/new_actor.html', form=form, actor=actor)

	@app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
	def edit_actor_submit(actor_id):
		# actor = Actor.query.get(actor_id)
		actor = Actor.query.filter(Actor.id==actor_id).one()
		form = ActorForm()
		error = False

		if form.validate_on_submit():
			try:
				actor.name = form.name.data
				actor.age = form.age.data
				actor.gender = form.gender.data
				actor.image_link = form.image_link.data

				# db.session.commit()
				actor.update()
				print('TRY')
			except:
				error = True
				print(sys.exc_info())
				actor.rollback()
			finally:
				# actor.close()
				print('FINALLY')
				if error:
					flash(
					'An error occurred. Actor '+'name'+' could not be added.'
					)
				else:
					print('NO ERROR')
					flash('Actor ' + 'name' + ' was successfully added!')
		else:
			print('ERROR')
			flash('One or more fields are not valid.')
			# flash(form.errors)
			return render_template('forms/new_actor.html', form=form, actor=actor)

		# return redirect(url_for('actors'))
		# return redirect(url_for('show_actor', actor_id=actor_id, _method='GET'))
		return render_template('pages/show_actor.html', actor=actor)
		# return redirect(url_for('index'))

	@app.route('/actors/<int:actor_id>', methods=['DELETE'])
	def delete_actor(actor_id):
		error = False
		actor = Actor.query.get(actor_id)
		actor_name = actor.name

		try:
			db.session.delete(actor)
			db.session.commit()
		except:
			error = True
			db.session.rollback()
		finally:
			db.session.close()

		if error:
			flash('An Error Occured')
		else:
			flash('Actor ' + actor_name + ' was successfully deleted!')

		return redirect(url_for('index'))


	return app

APP = create_app()

if __name__ == '__main__':
	APP.run(debug=True)
    # APP.run(host='0.0.0.0', port=8080, debug=True)