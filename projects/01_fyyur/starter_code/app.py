#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# DONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    artists = db.relationship('Artist', secondary=lambda: Show.__table__,
        backref=db.backref('Venue', lazy=True))

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__= 'Show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  finalVenuesList = []
  now = datetime.now()
  distinctCities = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
  for d in distinctCities:
    tempVenuesDict = {
      'city': d.city,
      'state': d.state,
      'venues': []
    }
    venuesInCity = Venue.query.filter_by(city=d.city, state=d.state).all()
    for v in venuesInCity:
      venueToAdd = {
        'id': v.id,
        'name': v.name,
        'num_upcoming_shows': Show.query.filter(Show.artist_id==v.id, Show.start_time > now).count()
      }
      tempVenuesDict['venues'].append(venueToAdd)
    finalVenuesList.append(tempVenuesDict)

  return render_template('pages/venues.html', areas=finalVenuesList);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = request.form.get('search_term', '')
  searchString = "%{}%".format(search)
  now = datetime.now()
  venuesMatching = Venue.query.filter(Venue.name.ilike(searchString))
  response = {
      'count': Venue.query.filter(Venue.name.ilike(searchString)).count(),
      'data': []
    }
  for venue in venuesMatching:
    venueDict = {
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': Show.query.filter(Show.venue_id == venue.id, Show.start_time > now).count()
    }
    response['data'].append(venueDict)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  venueObj = Venue.query.filter(Venue.id == venue_id).first()
  now = datetime.now()
  # lists to hold upcoming and past shows, to be populated below
  upcomingShows = []
  pastShows = []
  # list of all Show objects at given venue with id venue_id
  showsAtVenue = Show.query.filter(Show.venue_id == venue_id).all()
  
  #loops through all Show objects
  for show in showsAtVenue:
    #find artist object for show
    showArtist = Artist.query.filter(Artist.id == show.artist_id).first()
    #construct artist dict, same whether past of present show
    infoDict =  {
      'artist_id': show.artist_id,
      'artist_name': showArtist.name,
      'artist_image_link': showArtist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    #if upcoming show add to upcomingShows
    if show.start_time > now:
      upcomingShows.append(infoDict)
    #else add to pastShows
    else: 
      pastShows.append(infoDict)

  data = {
    'id': venue_id,
    'name': venueObj.name,
    'genres': list(venueObj.genres.split(' ')),
    'address': venueObj.address,
    'city': venueObj.city,
    'state': venueObj.state,
    'phone': venueObj.phone,
    'website': venueObj.website,
    'facebook_link': venueObj.facebook_link,
    'seeking_talent': venueObj.seeking_talent,
    'image_link': venueObj.image_link,
    'upcoming_shows': upcomingShows,
    'past_shows': pastShows, 
    'upcoming_shows_count': len(upcomingShows),
    'past_shows_count': len(pastShows)
  }

  if venueObj.seeking_talent == True:
    data['seeking_description'] = venueObj.seeking_description
  

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genresList = request.form.getlist('genres')
    genres = ' '.join(genresList)
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking = request.form.get('seeking_talent')
    seeking_talent = True
    if seeking == 'No':
      seeking_talent = False
      
    seeking_description = request.form.get('seeking_description')

    exists = db.session.query(db.session.query(Venue).filter_by(name=request.form['name']).exists()).scalar()

    if exists == False:
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website=website, seeking_description=seeking_description, seeking_talent=seeking_talent)
      db.session.add(venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Venue ' + request.form['name'] + ' already exists.')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except ValueError:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed!')
  finally:
    db.session.close()
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
  # DONE: replace with real data returned from querying the database
  data= Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search = request.form.get('search_term', '')
  searchString = "%{}%".format(search)
  now = datetime.now()
  artistsMatching = Artist.query.filter(Artist.name.ilike(searchString))
  response = {
    'count': Artist.query.filter(Artist.name.ilike(searchString)).count(),
    'data': []
  }
  for artist in artistsMatching:
    artistDict = {
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': Show.query.filter(Show.artist_id == artist.id, Show.start_time > now).count()
    }
    response['data'].append(artistDict)

  return render_template('pages/search_artists.html', results=response, search_term=search)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id
  artistObj = Artist.query.filter(Artist.id == artist_id).first()
  now = datetime.now()
  # lists to hold upcoming and past shows, to be populated below
  upcomingShows = []
  pastShows = []
  # list of all Show objects at given venue with id venue_id
  showsByArtist = Show.query.filter(Show.artist_id == artist_id).all()
  
  #loops through all Show objects
  for show in showsByArtist:
    #find venue object for show
    showVenue= Venue.query.filter(Venue.id == show.venue_id).first()
    #construct venue dict, same whether past of present show
    infoDict =  {
      'venue_id': show.venue_id,
      'venue_name': showVenue.name,
      'venue_image_link': showVenue.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    #if upcoming show add to upcomingShows
    if show.start_time > now:
      upcomingShows.append(infoDict)
    #else add to pastShows
    else: 
      pastShows.append(infoDict)

  data = {
    'id': artist_id,
    'name': artistObj.name,
    'genres': list(artistObj.genres.split(' ')),
    'city': artistObj.city,
    'state': artistObj.state,
    'phone': artistObj.phone,
    'website': artistObj.website,
    'facebook_link': artistObj.facebook_link,
    'seeking_venue': artistObj.seeking_venue,
    'image_link': artistObj.image_link,
    'upcoming_shows': upcomingShows,
    'past_shows': pastShows, 
    'upcoming_shows_count': len(upcomingShows),
    'past_shows_count': len(pastShows)
  }

  if artistObj.seeking_venue == True:
    data['seeking_description'] = artistObj.seeking_description
  

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # DONE: populate form with fields from artist with ID <artist_id>
  artist= Artist.query.filter(Artist.id == artist_id).first()
  form = ArtistForm(obj=artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genresList = request.form.getlist('genres')
    genres = ' '.join(genresList)
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking = True
    if request.form.get('seeking_venue') == 'No':
      seeking = False
    seeking_venue = seeking
    seeking_description = request.form.get('seeking_description')

    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.image_link = image_link
    artist.genres = genres
    artist.facebook_link = facebook_link
    artist.website = website
    artist.seeking_venue = seeking_venue
    artist.seeking_description = seeking_description

    db.session.add(artist)
    db.session.commit()
    # on successful db update, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  except ValueError:
    db.session.rollback()
    flash('An error occured. Artist ' + request.form['name'] + ' could not be updated.')
  finally: 
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # DONE: populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter(Venue.id == venue_id).first()
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genresList = request.form.getlist('genres')
    genres = ' '.join(genresList)
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking = request.form.get('seeking_talent')
    seeking_talent = True
    if seeking == 'No':
      seeking_talent = False
      
    seeking_description = request.form.get('seeking_description')

    venue.name = name
    venue.city = city
    venue.state = state
    venue.address = address
    venue.phone = phone
    venue.image_link = image_link
    venue.genres = genres
    venue.facebook_link = facebook_link
    venue.website = website
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description

    db.session.add(venue)
    db.session.commit()
    # on successful db update, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except ValueError: 
    db.session.rollback()
    flash('An error occured. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Artist record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genresList = request.form.getlist('genres')
    genres = ' '.join(genresList)
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking = True
    if request.form.get('seeking_venue') == 'No':
      seeking = False
    seeking_venue = seeking
    seeking_description = request.form.get('seeking_description')

    exists = db.session.query(db.session.query(Artist).filter_by(name=request.form['name']).exists()).scalar()

    if exists == False:
      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
    # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('Artist ' + request.form['name'] + ' already exists.')
  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  except ValueError:
    db.session.rollback()
    flash('An error occured. Artist ' + request.form['name'] + ' could not be listed.')
  finally: 
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  showsList = []
  for show in shows:
    showDict = {
      'venue_id': show.venue_id,
      'venue_name': Venue.query.filter_by(id = show.venue_id).first().name,
      'artist_id': show.artist_id,
      'artist_name': Artist.query.with_entities(Artist.name).filter_by(id = show.artist_id).first().name,
      'artist_image_link': Artist.query.filter_by(id = show.artist_id).first().image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    showsList.append(showDict)



  return render_template('pages/shows.html', shows=showsList)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except ValueError:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally: 
    db.session.close()
  return render_template('pages/home.html')

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
