import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/pedalsdb'
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
Manufacturer
'''
class Manufacturer(db.Model):
    __tablename__ = 'Manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    fb_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))

'''
Pedal
'''
class Pedal(db.Model):
    __tablename__ = 'Pedal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    pedal_type = db.Column(db.String(120))
    new_price = db.Column(db.String)
    used_price = db.Column(db.String)
    image_link = db.Column(db.String(500))



