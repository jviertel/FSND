import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/trivia'

db = SQLAlchemy()

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()
  CORS(app)
  return app

APP = create_app()
migrate = Migrate(APP, db)



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)