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

#Endpoint to handle GET requests for all Manufacturers
@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
  pass

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