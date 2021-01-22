import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Pedal, Manufacturer, setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  return app
  
APP = create_app()
db = setup_db(APP)
migrate = Migrate(APP, db)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)