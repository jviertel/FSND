import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {'origins': '*'}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Acess-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    if len(categories) == 0:
      abort(404)   

    categoriesDict = {}
    for c in categories:
      categoriesDict[c.id] = c.type

    return jsonify({
      'categories': categoriesDict,
      'num_categories': len(categories),
      'success': True
    })

  def paginate(questions, request, pg):
    firstItem = 10 * (pg -1)
    lastItem = firstItem + 10
    questions = [q.format() for q in questions] #Cite: 12/23/20 https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/af3a044c-37df-4ceb-8b0a-01c45cad6511/lessons/123d0a0a-8137-4e21-881f-8d03fb371209/concepts/7529c53d-c671-4ec7-bd7b-81ea374f72e3
    current_page = questions[firstItem:lastItem]

    return current_page
  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=['GET'])
  def get_questions():
    pg = request.args.get('page', 1, type=int)
    questionObjects = Question.query.all()
    current_page = paginate(questionObjects, request, pg)
    if len(questionObjects) == 0:
      abort(404)
    
    if pg > (len(questionObjects)/10 + 1):
      abort(404)

    questions = [q.format() for q in questionObjects] #Cite: 12/23/20 https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/af3a044c-37df-4ceb-8b0a-01c45cad6511/lessons/123d0a0a-8137-4e21-881f-8d03fb371209/concepts/7529c53d-c671-4ec7-bd7b-81ea374f72e3

    categories = Category.query.all()
    categoriesDict = {}
    for c in categories:
      categoriesDict[c.id] = c.type

    return jsonify({
      'questions': current_page,
      'num_questions': len(questions),
      'categories': categoriesDict, 
      'current_category': None,
      'success': True,

    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    toDelete = Question.query.filter(Question.id == question_id).one_or_none()
    if toDelete == None:
      abort(404)
    
    try:
      toDelete.delete()
      Question.session.commit()
    except Exception:
      Question.session.rollback()
    finally:
      Question.session.close()


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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

  
  return app

    