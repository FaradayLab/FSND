# import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def format_categories():
  return {cat.id:cat.type for cat in Category.query.all()}

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  @app.route('/categories')
  def get_categories():
    categories = format_categories()

    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  @TODO: 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    categories = format_categories()
    selection = Question.query.all()
    questions = paginate_questions(request, selection)

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(Question.query.all()),
      'categories': categories,
      'current_category': None
    })
  '''
  @TODO:
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id = question_id).one_or_none()

    if question:
      question.delete()
    else:
      abort(404)

    return jsonify({'success':True})
  '''
  @TODO: 
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()
    new_question = data['question']
    new_answer = data['answer']
    new_difficulty = data['difficulty']
    new_category = data['category']

    # print('\n')
    # print('\n')
    # print(f'{data}')
    # print('\n')
    # print('\n')
    if new_question and new_answer:
      question = Question(
        question = new_question,
        answer = new_answer,
        difficulty = new_difficulty,
        category = new_category
      )
      question.insert()

      return jsonify({
        'success': True
      })
    else:
      abort(400)

  '''
  @TODO: 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm']

    if search_term:
      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
      questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(selection.all()),
        'current_category': None
      })
    else:
      abort(400)
  '''
  @TODO:
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def questions_by_cat(category_id):
    selection = Question.query.filter_by(category = category_id).all()
    questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(selection),
      'current_category': category_id
    })

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
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    data = request.get_json()
    previous_questions = data['previous_questions']
    quiz_category = data['quiz_category']
    category_id = quiz_category['id']


    '''
    When starting new quiz check for category. If ALL, get question whose ID in not in previous questions
    If Specific category get ID of all questions in category, select ID, check if ID is in previous questions
    '''

    if quiz_category['id']:
      query = Question.query.filter(Question.category == category_id).all()
    else:
      query = Question.query.all()
    
    if len(previous_questions) >= len(query):
      question = None
      q_id = 'none'
      # abort(404)
      print('length of prev questions', len(previous_questions), 'as long as than query', len(query))
    else:
      question = query[random.randint(0, len(query) - 1)].format()
      i = 1
      while question['id'] in previous_questions:
        question = query[random.randint(0, len(query) - 1)].format()

      q_id = question['id']

    print('\n')
    print('\n')
    print(f'{previous_questions}')
    print(f'{q_id}')
    # print(len(previous_questions))
    print('\n')
    print('\n')
    return jsonify({
      'success': True,
      'question': question
    })
      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable Entity"
    }), 422
  return app

    