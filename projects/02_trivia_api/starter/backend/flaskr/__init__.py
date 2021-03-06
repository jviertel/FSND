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

  def paginate(questions, request):
    pg = request.args.get('page', 1, type=int)
    if len(questions) == 0:
      abort(404)

    if pg > (len(questions)/10 + 1): 
      abort(404)
    firstItem = 10 * (pg -1)
    lastItem = firstItem + 10
    questions = [q.format() for q in questions] #Cite: 12/23/20 https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/af3a044c-37df-4ceb-8b0a-01c45cad6511/lessons/123d0a0a-8137-4e21-881f-8d03fb371209/concepts/7529c53d-c671-4ec7-bd7b-81ea374f72e3
    current_page = questions[firstItem:lastItem]

    return current_page

  def list_categories():
    categories = Category.query.all()
    categoriesDict = {}
    for c in categories:
      categoriesDict[c.id] = c.type
    return categoriesDict

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

    return jsonify({
      'categories': list_categories(),
      'num_categories': len(categories),
      'success': True
    })

 
    
    
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
    
    questionObjects = Question.query.all()
    current_page = paginate(questionObjects, request)

    return jsonify({
      'questions': current_page,
      'total_questions': len(questionObjects),
      'categories': list_categories(), 
      'current_category': None,
      'success': True,
    })

  '''
  @DONE: 
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
      questions = Question.query.all()
      current_page = paginate(questions, request)
    except Exception:
      abort(422)
    
    return jsonify({
      'deleted_question': question_id,
      'questions': current_page, 
      'total_questions': len(questions),
      'categories': list_categories(),
      'current_category': None, 
      'success': True
    })


  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    question_text = body.get('question', None)
    answer_text = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    try:
          question = Question(question=question_text, answer=answer_text, difficulty=difficulty, category=category)
          question.insert()

          questions = Question.query.all()
          current_page = paginate(questions, request)

          return jsonify({
            'created_question': question.id, 
            'questions': current_page, 
            'total_questions': len(questions),   
            'categories': list_categories(),
            'current_category': None,
            'success': True
          })
    except Exception: 
      abort(422)

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    searchString = "%{}%".format(search_term) #Cite: 12/19/20 https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring
    questionObjects = Question.query.filter(Question.question.ilike(searchString)).all()
    if len(questionObjects) == 0:
      abort(404)
    current_page = paginate(questionObjects, request)
    return jsonify({
      'questions': current_page,
      'total_questions': len(questionObjects),
      'categories': list_categories(),
      'current_category': None,
      'success': True
    })

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    categories = list_categories()
    if category_id not in categories:
      abort(404)


    questions = Question.query.filter(Question.category == category_id).all()

    current_page = paginate(questions, request)

    return jsonify({
        'questions': current_page,
        'total_questions': len(questions),
        'current_category': category_id,
        'success': True,
      })


  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/quizzes", methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    category = body.get('quiz_category', None)

    categories = list_categories()
    quiz_questions = []
    if category != None:
      if category['id'] == 0:
        questions = Question.query.all()
      elif int(category['id']) > 0 and int(category['id']) < len(categories) + 1:
        questions = Question.query.filter(Question.category == category['id']).all()
      else:
        abort(422)
      for q in questions:
        if q.id not in previous_questions:
          quiz_questions.append(q.format())
      
      if len(quiz_questions) == 0:
        return jsonify({
          'question': False,
          'success': False
        })
      else:
        current_question = random.choice(quiz_questions) #Cite: 12/26/2020 https://knowledge.udacity.com/questions/234306
        return jsonify({
          'question': current_question,
          'success': True
        })
        
    else:
      abort(400)

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

    