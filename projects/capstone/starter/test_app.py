import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Pedal, Manufacturer, setup_db

class TestPedalsAPI(unittest.TestCase):

    def setUp(self):
        '''Run before tests'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/pedalsdb_test'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        '''Run after tests'''
        pass
    
    #Test successful get request to /manufacturers endpoint
    def test_get_manufacturers(self):
        res = self.client().get('/manufacturers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['num_manufacturers'])
        self.assertTrue(len(data['manufacturers']))
        self.assertEqual(data['success'], True)

    #Test 404 for page out of bounds
    def test_manufacturers_404_page_out_of_bounds(self):
        res = self.client().get('/manufacturers?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test successful get request to /manufacturers/5/pedals
    def test_get_pedals_by_manufacturer(self):
        res = self.client().get('/manufacturers/5/pedals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['manufacturer_id'], 5)
        self.assertTrue(data['manufacturer_name'])
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])    
        self.assertEqual(data['success'], True)
    
    #Test 404 for page out of bounds
    def test_404_manufacturer_not_exists(self):
        res = self.client().get('/manufacturers/5000/pedals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    #Test successful post request to /manufacturers
    def test_post_manufacturer(self):
        res = self.client().post('/manufacturers', 
            json = {
                'name': 'Volcanic Audio',
                'website_link': 'https://www.volcanicaudio.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_manufacturer'])
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)

    #Test unsuccessful post request entry already exists to /manufacturers
    def test_manufacturer_already_exists(self):
        res = self.client().post('/manufacturers',
            json = {
                'name': 'Boss',
                'website_link': 'https://www.bossaudio.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_manufacturer'], None)
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], False)
    
    



if __name__ == '__main__':
    unittest.main()
