import os
import shutil
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# def navigate_and_rename(src):
#     for item in os.listdir(src):
#         s = os.path.join(src, item)
#         if os.path.isdir(s):
#             navigate_and_rename(s)
#         else if s.endswith(".html"):
#             shutil.copy(s, os.path.join(src, "newname.html"))    

'''
When adding new category this creates a new category image to be 
displayed along with the category name using a generic category 
image added to the public folder
'''
def create_category_image(new_file_name):
    img_path= os.path.join(os.curdir , "../frontend/public")
    src_img= os.path.join(img_path, 'generic-category.svg')
    dst_img= os.path.join(img_path+'/', new_file_name+'.svg')
    shutil.copy(src_img, dst_img)

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def formatted_categories():
    return {cat.id: cat.type for cat in Category.query.all()}


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
        categories = formatted_categories()

        return jsonify({'success': True, 'categories': categories})

    '''
    Add Categories
    '''
    @app.route('/categories', methods=['POST'])
    def create_category():
        query = Category.query.all()
        new_type = request.get_json()['type']

        for cat in query:

            if cat.type.lower() == new_type.lower():
                abort(422)

        category = Category(type=new_type)
        categories = formatted_categories()

        category.insert()
        

        create_category_image(new_type)

        return jsonify({'success': True, 'categories': categories})

    @app.route('/questions')
    def get_questions():
        categories = formatted_categories()
        selection = Question.query.all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': questions,
                'total_questions': len(Question.query.all()),
                'categories': categories,
                'current_category': None,
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({'success': True})
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        new_question = data['question']
        new_answer = data['answer']
        new_difficulty = data['difficulty']
        new_category = data['category']

        if new_question and new_answer:
            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify({'success': True})
            except:
                abort(422)
        else:
            abort(400)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json()['searchTerm']

        if search_term:
            try:
                selection = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
                questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        'success': True,
                        'questions': questions,
                        'total_questions': len(selection.all()),
                        'current_category': None,
                    }
                )
            except:
                abort(422)
        else:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def questions_by_cat(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, selection)

        return jsonify(
            {
                'success': True,
                'questions': questions,
                'total_questions': len(selection),
                'current_category': category_id,
            }
        )

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        previous_questions = request.get_json()['previous_questions']
        category_id = request.get_json()['quiz_category']['id']
        try:
            if category_id:
                questions = (
                    Question.query.filter_by(category=category_id)
                    .filter(Question.id.notin_(previous_questions))
                    .all()
                )
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

            length_of_questions = len(questions)

            if length_of_questions > 0:
                question = questions[random.randrange(0, length_of_questions)].format()
            else:
                question = None

            return jsonify({'success': True, 'question': question})
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "Internal Server Error"}), 500

    return app
