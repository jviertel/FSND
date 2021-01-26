import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Pedal, Manufacturer, setup_db
from auth import AuthError, requires_auth

#Configure app
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  #Helper functions
  def paginate(objects, request):
      pg = request.args.get('page', 1, type=int)
      if len(objects) == 0:
        abort(404)

      if pg > (len(objects)/20 + 1): 
        abort(404)
      firstItem = 20 * (pg -1)
      lastItem = firstItem + 20
      objects = [o.format() for o in objects] #Cite: 1/23/20 https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/af3a044c-37df-4ceb-8b0a-01c45cad6511/lessons/123d0a0a-8137-4e21-881f-8d03fb371209/concepts/7529c53d-c671-4ec7-bd7b-81ea374f72e3
      current_page = objects[firstItem:lastItem]

      return current_page

  #Endpoint to handle GET requests for all Manufacturers
  @app.route('/manufacturers', methods=['GET'])
  def get_manufacturers():
    manufacturer_objects = Manufacturer.query.order_by(Manufacturer.id).all()
    
    if len(manufacturer_objects) == 0:
      abort(404)
    
    current_page = paginate(manufacturer_objects, request)
    
    return jsonify({
      'manufacturers': current_page,
      'num_manufacturers': len(manufacturer_objects),
      'success': True
    })
    

  #Endpoint to handle GET requests for pedals by manufacturer
  @app.route('/manufacturers/<int:manufacturer_id>/pedals', methods=['GET'])
  def get_pedals_by_manufacturer(manufacturer_id):
    pedals_by_manufacturer_objects = Pedal.query.filter(Pedal.manufacturer_id == manufacturer_id).all()
    manufacturer = Manufacturer.query.filter(Manufacturer.id == manufacturer_id).first()

    if manufacturer is None:
      abort(404) 
    
    manufacturer_name = manufacturer.name

    if len(pedals_by_manufacturer_objects) == 0:
      abort(404)
    
    current_page = paginate(pedals_by_manufacturer_objects, request)

    return jsonify({
      'manufacturer_id': manufacturer_id,
      'manufacturer_name': manufacturer_name,
      'pedals': current_page,
      'num_pedals': len(pedals_by_manufacturer_objects),
      'success': True
    })

  #Endpoint to handle POST requests for new manufacturer
  @app.route('/manufacturers', methods=['POST'])
  @requires_auth('post:manufacturers')
  def create_manufacturer(payload):
    body = request.get_json()
    name = body.get('name', None)
    website_link = body.get('website_link', None)
    try:
      manufacturer = Manufacturer(name=name, website_link=website_link)
      exists = Manufacturer.query.filter(Manufacturer.name == name).one_or_none()
      if exists == None:
        manufacturer.insert()

        manufacturers = Manufacturer.query.all()
        current_page = paginate(manufacturers, request)

        return jsonify({
          'created_manufacturer': manufacturer.id,
          'manufacturers': current_page,
          'num_manufacturers': len(manufacturers),
          'success': True
        })
      else:
        manufacturers = Manufacturer.query.all()
        current_page = paginate(manufacturers, request)

        return jsonify({
          'created_manufacturer': None,
          'manufacturers': current_page,
          'num_manufacturers': len(manufacturers),
          'success': False  
        })
    except Exception: 
      abort(422)

    

  #Endpoint to handle POST requests for new pedal
  @app.route('/pedals', methods=['POST'])
  @requires_auth('post:pedals')
  def create_pedals(payload):
    body = request.get_json()
    name = body.get('name', None)
    pedal_type = body.get('pedal_type', None)
    new_price = body.get('new_price', None)
    used_price = body.get('used_price', None)
    manufacturer_id = body.get('manufacturer_id', None)

    try:
      pedal = Pedal(name=name, pedal_type=pedal_type, new_price=new_price, used_price=used_price, manufacturer_id=manufacturer_id)
      exists = Pedal.query.filter(Pedal.name == name).one_or_none()
      if exists == None:
        pedal.insert()

        pedals = Pedal.query.all()
        current_page = paginate(pedals, request)

        return jsonify({
          'created_pedal': pedal.id,
          'pedals': current_page,
          'num_pedals': len(pedals),
          'success': True
        })
      else:
        pedals = Pedal.query.all()
        current_page = paginate(pedals, request)

        return jsonify({
          'created_pedal': None,
          'pedals': current_page,
          'num_pedals': len(pedals),
          'success': False  
        })
    except Exception: 
      abort(422)

  #Endpoint to handle PATCH requests for manufacturers
  @app.route('/manufacturers/<int:manufacturer_id>', methods=['PATCH'])
  @requires_auth('patch:manufacturers')
  def update_manufacturers(payload, manufacturer_id):
    body = request.get_json()
    name = body.get('name', None)
    website_link = body.get('website_link', None)

    manufacturer = Manufacturer.query.filter(Manufacturer.id == manufacturer_id).one_or_none()

    if manufacturer is None:
      abort(404)
    
    manufacturer.name = name
    manufacturer.website_link = website_link

    manufacturer.update()

    manufacturers = Manufacturer.query.all()
    current_page = paginate(manufacturers, request)

    return jsonify({
      'updated_manufacturer': manufacturer.id,
      'manufacturers': current_page,
      'num_manufacturers': len(manufacturers),
      'success': True
    })


  #Endpoint to handle PATCH requests for pedals
  @app.route('/pedals/<int:pedal_id>', methods=['PATCH'])
  @requires_auth('patch:pedals')
  def update_pedals(payload, pedal_id):
    body = request.get_json()
    name = body.get('name', None)
    pedal_type = body.get('pedal_type', None)
    new_price = body.get('new_price', None)
    used_price = body.get('used_price', None)
    manufacturer_id = body.get('manufacturer_id', None)

    pedal = Pedal.query.filter(Pedal.id == pedal_id).one_or_none()

    if pedal is None:
      abort(404)
    
    pedal.name = name
    pedal.pedal_type = pedal_type
    pedal.new_price = new_price
    pedal.used_price = used_price
    pedal.manufacturer_id =  manufacturer_id

    pedal.update()

    pedals = Pedal.query.all()
    current_page = paginate(pedals, request)

    return jsonify({
      'updated_pedal': pedal.id,
      'pedals': current_page,
      'num_pedals': len(pedals),
      'success': True
    })

  #Endpoint to handle DELETE requests for manufacturers
  @app.route('/manufacturers/<int:manufacturer_id>', methods=['DELETE'])
  @requires_auth('delete:manufacturers')
  def delete_manufacturer(payload, manufacturer_id):
    manufacturer = Manufacturer.query.filter(Manufacturer.id == manufacturer_id).one_or_none()
    if manufacturer is None:
      abort(404)
    try:
      manufacturer.delete()
      manufacturers = Manufacturer.query.all()
      current_page = paginate(manufacturers, request)
    except Exception:
      abort(422)
    
    return jsonify({
      'deleted_manufacturer': manufacturer_id,
      'manufacturers': current_page,
      'num_manufacturers': len(manufacturers),
      'success': True
    })

  #Endpoint to handle DELETE requests for pedals
  @app.route('/pedals/<int:pedal_id>', methods=['DELETE'])
  @requires_auth('delete:pedals')
  def delete_pedals(payload, pedal_id):
    pedal = Pedal.query.filter(Pedal.id == pedal_id).one_or_none()
    if pedal is None:
      abort(404)
    try:
      pedal.delete()
      pedals = Pedal.query.all()
      current_page = paginate(pedals, request)
    except Exception:
      abort(422)
    
    return jsonify({
      'deleted_pedal': pedal_id,
      'pedals': current_page,
      'num_pedals': len(pedals),
      'success': True
    })

  #Error handlers
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'error': 400,
      'success': False,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      'error': 404,
      'success': False, 
      'message': 'resource was not found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'error': 405,
      'success': False,
      'message': 'method not allowed'
    })

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'error': 422,
      'success': False,
      'message': 'unprocessable entity'
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'error': 500,
      'success': False,
      'message': 'internal server error'
    }), 500
  
  @app.errorhandler(AuthError)
  def authentication_error(error):
      return jsonify(error.error), error.status_code
      # Cite: 1/11/2021 https://knowledge.udacity.com/questions/204223

  
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)