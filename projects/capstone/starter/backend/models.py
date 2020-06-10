import os
# DATE OBJECT FOR REALASE DATE?
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_path = os.environ['DATABASE_URL']
database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "casting"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Person
Have title and release year
'''
class Movie(db.Model):  
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release = Column(Date, nullable=False) #DATE OBJECT?

    def __init__(self, name, release=""):
        self.name = name
        self.release = release

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'release': self.release
        }

class Actor(db.Model):  
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String(1), nullable=False)
    age = Column(Integer, nullable=False)

    def __init__(self, name, gender=""):
        self.name = name
        self.gender = gender
        self.age = age

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }
