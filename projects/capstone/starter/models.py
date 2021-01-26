import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/pedalsdb_test'
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
Manufacturer
'''
class Manufacturer(db.Model):
    __tablename__ = 'Manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120)) 
    website_link = db.Column(db.String(500))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'website_link': self.website_link
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Pedal.id', ondelete='CASCADE'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'pedal_type': self.pedal_type,
            'new_price': self.new_price,
            'used_price': self.used_price,
            'manufacturer_id': self.manufacturer_id
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


