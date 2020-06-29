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
    image_link = Column(String)

    def __init__(self, title, release, image_link):
        self.title = title
        self.release = release
        self.image_link = image_link

    def format(self):
        return {
            'id': self.id,
            'name': self.title,
            'release': self.release,
            'image_link': self.image_link
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

class Actor(db.Model):  
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(2), nullable=False)
    image_link = Column(String)

    def __init__(self, name, age, gender, image_link):
        self.name = name
        self.age = age
        self.gender = gender
        self.image_link = image_link

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image_link': self.image_link
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
        
    def close(self):
        db.session.close()