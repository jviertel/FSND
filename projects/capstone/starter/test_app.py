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

    #Test post request to /manufacturers
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
    
    #Test post request to /pedals
    def test_post_pedal(self):
        res = self.client().post('/pedals',
            json = {
                'name': 'California Surf',
                'pedal_type': 'Reverb',
                'new_price': '$99.00',
                'used_price': '$65.00',
                'manufacturer_id': 37
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_pedal'])
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)

    #Test unsuccessful post request entry already exists to /pedals
    def test_pedal_already_exists(self):
        res = self.client().post('/pedals',
            json = {
                'name': 'Afterglow',
                'pedal_type': 'Chorus',
                'new_price': '$69.00',
                'used_price': '$39.00',
                'manufacturer_id': 43
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_pedal'], None)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], False)

    #Test patch request to /manufacturers/37
    def test_update_manufacturer(self):
        res = self.client().patch('/manufacturers/37',
            json = {
                'name': 'Changed Name',
                'website_link': 'https://www.pedals.info.com'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_manufacturer'], 37)
        self.assertTrue(len(data['manufacturers']))
        self.assertTrue(data['num_manufacturers'])
        self.assertEqual(data['success'], True)
    
    #Test unsuccessful patch request not found to /manufacturers/5000
    def test_patch_404_manufacturer_not_exists(self):
        res = self.client().patch('/manufacturers/5000',
            json = {
                'name': 'Changed Name',
                'website_link': 'https://www.pedals.info.com'
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
    
    #Test patch request to /pedals/472
    def test_update_pedals(self):
        res = self.client().patch('/pedals/472',
            json = {
                'name': 'Hot Rod',
                'pedal_type': 'Distortion',
                'new_price': '$79.00',
                'used_price': '$45.00',
                'manufacturer_id': 25
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_pedal'], 472)
        self.assertTrue(len(data['pedals']))
        self.assertTrue(data['num_pedals'])
        self.assertEqual(data['success'], True)
    
    #Test unsuccessful patch request not found to /pedals/5000
    def test_patch_404_pedal_not_exists(self):
        res = self.client().patch('/pedals/5000',
            json = {
                'name': 'Hot Rod',
                'pedal_type': 'Distortion',
                'new_price': '$79.00',
                'used_price': '$45.00',
                'manufacturer_id': 25
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
        


if __name__ == '__main__':
    unittest.main()
