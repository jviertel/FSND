import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Pedal, Manufacturer, setup_db

#Configure app
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  return app
  
app = create_app()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

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
  manufacturerObjects = Manufacturer.query.order_by(Manufacturer.id).all()
  
  if len(manufacturers) == 0:
    abort(404)
  
  current_page = paginate(manufacturerObjects, request)
  
  return jsonify({
    'manufacturers': current_page,
    'num_manufacturers': len(manufacturerObjects),
    'success': True
  })
  

#Endpoint to handle GET requests for pedals by manufacturer
@app.route('/manufacturers/<int:manufacturer_id>/pedals', methods=['GET'])
def get_pedals_by_manufacturer(manufacturer_id):
  pass

#Endpoint to handle POST requests for new manufacturer
@app.route('/manufacturers', methods=['POST'])
def create_manufacturers():
  pass

#Endpoint to handle POST requests for new pedal
@app.route('/pedals', methods=['POST'])
def create_pedals():
  pass

#Endpoint to handle PATCH requests for manufacturers
@app.route('/manufacturers/<int:manufacturer_id>', methods=['PATCH'])
def update_manufacturers(manufacturer_id):
  pass

#Endpoint to handle PATCH requests for pedals
@app.route('/pedals/<int:pedal_id>', methods=['PATCH'])
def update_pedals(pedal_id):
  pass

#Endpoint to handle DELETE requests for manufacturers
@app.route('/manufacturers/<int:manufacturer_id>', methods=['DELETE'])
def delete_manufacturer(manufacturer_id):
  pass

#Endpoint to handle DELETE requests for pedals
@app.route('/pedals/<int:pedal_id>', methods=['DELETE'])
def delete_pedals(pedal_id):
  pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)