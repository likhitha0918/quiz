from . import db
from flask_login import UserMixin

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Easy
    science_computers = db.Column(db.Integer)
    mythology = db.Column(db.Integer)
    sports = db.Column(db.Integer)
    vehicles = db.Column(db.Integer)
    general_knowledge = db.Column(db.Integer)
    # Medium
    science_computers_medium = db.Column(db.Integer)
    mythology_medium = db.Column(db.Integer)
    sports_medium = db.Column(db.Integer)
    vehicles_medium = db.Column(db.Integer)
    general_knowledge_medium = db.Column(db.Integer)
    # Hard
    science_computers_hard = db.Column(db.Integer)
    mythology_hard = db.Column(db.Integer)
    sports_hard = db.Column(db.Integer)
    vehicles_hard = db.Column(db.Integer)
    general_knowledge_hard = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    scores = db.relationship('Scores')

