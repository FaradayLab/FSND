#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import psycopg2
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id                   = db.Column(db.Integer, primary_key=True)
  name                 = db.Column(db.String)
  city                 = db.Column(db.String(120))
  state                = db.Column(db.String(120))
  address              = db.Column(db.String(120))
  phone                = db.Column(db.String(120))
  facebook_link        = db.Column(db.String(120))
  image_link           = db.Column(db.String(500))
  website              = db.Column(db.String(120))
  genres               = db.Column(db.ARRAY(db.String()))
  seeking_talent       = db.Column(db.Boolean, default=False)
  seeking_description  = db.Column(db.String(500))
  # past_shows           = db.Column(db.ARRAY)
  # upcoming_shows       = db.Column(db.ARRAY)
  # past_shows_count     = db.Column(db.Integer)
  # upcoming_shows_count = db.Column(db.Integer)

  # artists = db.relationship('Artist', secondary = 'Show')
  artists                = db.relationship('Show', backref='venue', lazy=True)

  def get_venue(self):
    return {
      'id': self.id,
      'name': self.name
    }
  def __repr__(self):
    return f'<Venue ID: {self.id}, name: {self.name}>'

class Artist(db.Model):
  __tablename__ = 'Artist'

  id                   = db.Column(db.Integer, primary_key=True)
  name                 = db.Column(db.String)
  city                 = db.Column(db.String(120))
  state                = db.Column(db.String(120))
  phone                = db.Column(db.String(120))
  facebook_link        = db.Column(db.String(120))
  image_link           = db.Column(db.String(500))
  website              = db.Column(db.String(120))
  genres               = db.Column(db.ARRAY(db.String()))
  seeking_venue        = db.Column(db.Boolean, default=False)
  seeking_description  = db.Column(db.String(500))
  # past_shows           = db.Column(db.ARRAY)
  # upcoming_shows       = db.Column(db.ARRAY)
  # past_shows_count     = db.Column(db.Integer)
  # upcoming_shows_count = db.Column(db.Integer)

  # venues = db.relationship('Venue', secondary= 'Show')
  venues                = db.relationship('Show', backref='artist', lazy=True)

  def __repr__(self):
      return f'<Artist ID: {self.id}, name: {self.name}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  id         = db.Column(db.Integer, primary_key=True)
  artist_id  = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  venue_id   = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)

  # venue = db.relationship('Venue')
  # artist = db.relationship('Artist')

  def __repr__(self):
      return '<Show {}>'.format(self.artist_id, self.venue_id)

# db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  data = {
    'artist' : Artist.query.order_by(Artist.id.desc()).limit(2),
    'venue'  : Venue.query.order_by(Venue.id.desc()).limit(2)
    }
  return render_template('pages/home.html', recent=data)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  areas = Venue.query.distinct('city','state').all()

  data = []
  for area in areas:
    venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
    record = {
      'city': area.city,
      'state': area.state,
      'venues': [venue.get_venue() for venue in venues],
    }
    data.append(record)
  
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  term = request.form.get('search_term', '')
  query = Venue.query.filter(Venue.name.ilike('%'+term+'%'))
  data = []
  for venue in query:
    data.append({
      'id'   : venue.id,
      'name' : venue.name
    })
    
  response = {
    'count' : query.count(),
    'data'  : data
  }
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data                 = Venue.query.get(venue_id)
  shows                = Show.query.join(Artist).filter(Show.venue_id==venue_id)
  upcoming_shows       = []
  upcoming_shows_count = 0
  past_shows           = []
  past_shows_count     = 0

  for show in shows:
    artist_info = { 
        'artist_id': show.artist.id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': str(show.start_time)
      }
    if show.start_time > datetime.now():
      upcoming_shows_count += 1
      upcoming_shows.append(artist_info)
    else:
      past_shows_count += 1
      past_shows.append(artist_info)

  data.upcoming_shows       = upcoming_shows
  data.upcoming_shows_count = upcoming_shows_count
  data.past_shows           = past_shows
  data.past_shows_count     = past_shows_count

# WAS FULL VENUE DATA AND FUNCTION

  return render_template('pages/show_venue.html', venue=data)

  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False

  try:
    new_venue              = Venue(
      name                 = request.form['name'],
      city                 = request.form['city'],
      state                = request.form['state'],
      address              = request.form['address'],
      phone                = request.form['phone'],
      genres               = request.form.getlist('genres'),
      seeking_artist       = False if request.form.get('seeking_artist') == None else True,
      seeking_description  = request.form['seeking_description'],
      image_link           = request.form['image_link'],
      website              = request.form['website'],
      facebook_link        = request.form['facebook_link'],
    )
    db.session.add(new_venue)
    db.session.commit()
  except :
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  
  for artist in artists:
    info = {
      'id'   : artist.id,
      'name' : artist.name
    }
    data.append(info)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  term = request.form.get('search_term', '')
  query = Artist.query.filter(Artist.name.ilike('%'+term+'%'))
  data = []
  for artist in query:
    data.append({
      'id'   : artist.id,
      'name' : artist.name
    })

  response = {
    'count' : query.count(),
    'data'  : data
  }
  # response={
  #   "count"               : 1,
  #   "data"                : [{
  #     "id"                : 1,
  #     "name"              : "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist                 = Artist.query.get(artist_id)
  shows                = Show.query.join(Venue).filter(Show.artist_id==artist_id)
  upcoming_shows       = []
  upcoming_shows_count = 0
  past_shows           = []
  past_shows_count     = 0

  for show in shows:
    venue_info = { 
        'venue_id'        : show.venue.id,
        'venue_name'      : show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time'      : str(show.start_time)
      }
    if show.start_time > datetime.now ():
      upcoming_shows_count += 1
      upcoming_shows.append(venue_info)
    else:
      past_shows_count += 1
      past_shows.append(venue_info)

  artist.upcoming_shows       = upcoming_shows
  artist.upcoming_shows_count = upcoming_shows_count
  artist.past_shows           = past_shows
  artist.past_shows_count     = past_shows_count

  return render_template('pages/show_artist.html', artist=artist)

  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form   = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)
  error  = False
  try:
    artist.name                = request.form['name']
    artist.city                = request.form['city']
    artist.state               = request.form['state']
    artist.phone               = request.form['phone']
    artist.genres              = request.form.getlist('genres')
    artist.seeking_venue       = False if request.form.get('seeking_venue') == None else True
    artist.seeking_description = request.form['seeking_description']
    artist.image_link          = request.form['image_link']
    artist.website             = request.form['website']
    artist.facebook_link       = request.form['facebook_link']

    db.session.commit()
  except :
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form  = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  error  = False
  try:
    venue.name                = request.form['name']
    venue.city                = request.form['city']
    venue.state               = request.form['state']
    venue.phone               = request.form['phone']
    venue.genres              = request.form.getlist('genres')
    venue.seeking_artist      = False if request.form.get('seeking_artist') == None else True
    venue.seeking_description = request.form['seeking_description']
    venue.image_link          = request.form['image_link']
    venue.website             = request.form['website']
    venue.facebook_link       = request.form['facebook_link']

    db.session.commit()
  except :
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False

  try:
    new_artist = Artist(
      name                = request.form['name'],
      city                = request.form['city'],
      state               = request.form['state'],
      phone               = request.form['phone'],
      genres              = request.form.getlist('genres'),
      seeking_venue       = False if request.form.get('seeking_venue') == None else True,
      seeking_description = request.form['seeking_description'],
      image_link          = request.form['image_link'],
      website             = request.form['website'],
      facebook_link       = request.form['facebook_link']
    )
    db.session.add(new_artist)
    db.session.commit()
  except :
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.order_by('start_time').all()
  data = []
  for show in shows:
    data.append({
      'venue_id': show.venue.id,
      'venue_name': show.venue.name,
      'artist_id': show.artist.id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False

  try:
    new_show = Show(
      artist_id  = request.form['artist_id'],
      venue_id   = request.form['venue_id'],
      start_time = request.form['start_time']
    )
    db.session.add(new_show)
    db.session.commit()
  except :
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
        flash('An error occurred. The show could not be listed.')
    else:
        flash('Show was successfully listed!')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')
  return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''