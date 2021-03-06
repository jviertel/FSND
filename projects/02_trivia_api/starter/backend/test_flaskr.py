import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:88c67e0d53bef241b661e0e3a6cb0cd1@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    ''
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['num_categories'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)
        self.assertEqual(data['success'], True)

    def test_404_page_out_of_bounds(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/21')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_question'], 21)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)
        self.assertEqual(data['success'], True)

    def test_404_question_id_invalid(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
    
    def test_create_question(self):
        res = self.client().post('/questions', 
            json={
                'question': 'How many NBA championships have the Chicago Bulls won?',
                'answer': '6',
                'difficulty': 2, 
                'category': 2
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created_question'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)
        self.assertEqual(data['success'], True)

    def test_search_question(self):
        res = self.client().post('/questions/search',
            json={'searchTerm': 'What'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)
        self.assertEqual(data['success'], True)
    
    def test_search_no_results(self):
        res = self.client().post('/questions/search', 
            json={
                'searchTerm': 'asflhasodifhdslflasdf'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')

    def get_qeustions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 4)
        self.assertEqual(data['success'], True)
    
    def test_category_id_invalid(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource was not found')
    
    def test_play_quiz(self):
        res = self.client().post('/quizzes', 
            json = {
                'previous_questions': [],
                'quiz_category': {
                    'id': 4
                }
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)
    
    def test_play_quiz_invalid_category(self):
        res = self.client().post('/quizzes',
            json = {
                'previous_question': [],
                'quiz_category': {
                    'id': 100
                }
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()