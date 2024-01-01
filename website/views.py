from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from .models import Scores
from . import db
from .fetcher_funcs import fetcher, check_correct_answers


class Question():
    def __init__(self, question, option_1, option_2, option_3, option_4, id):
        self.question = question
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.id = id
        




views = Blueprint('views', __name__)

# Global Variables
answers = None
questions = None
category = None
difficulty = None
#################

@views.route('/')
def home():
    return render_template('index.html', user=current_user)


@views.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    score = request.form.get('score')
    global category
    global difficulty
    if score:
        id = current_user.id
        current_scores = Scores.query.filter_by(user_id = id).first()
        if difficulty == 'easy':
            if category == 'science_computers':
                current_scores.science_computers = score
            if category == 'mythology':
                current_scores.mythology = score
            if category == 'sports':
                current_scores.sports = score
            if category == 'vehicles':
                current_scores.vehicles = score
            if category == 'general_knowledge':
                current_scores.general_knowledge = score
        if difficulty == 'medium':
            if category == 'science_computers':
                current_scores.science_computers_medium = score
            if category == 'mythology':
                current_scores.mythology_medium = score
            if category == 'sports':
                current_scores.sports_medium = score
            if category == 'vehicles':
                current_scores.vehicles_medium = score
            if category == 'general_knowledge':
                current_scores.general_knowledge_medium = score
        if difficulty == 'hard':
            if category == 'science_computers':
                current_scores.science_computers_hard = score
            if category == 'mythology':
                current_scores.mythology_hard = score
            if category == 'sports':
                current_scores.sports_hard = score
            if category == 'vehicles':
                current_scores.vehicles_hard = score
            if category == 'general_knowledge':
                current_scores.general_knowledge_hard = score
        db.session.commit()
        
    return render_template('profile.html', user=current_user)

@views.route('/quiz')
@login_required
def quiz():
    global questions
    if questions != None:
        
        return render_template('quiz.html', user=current_user, questions=questions)
    else:
        return redirect(url_for('views.pick_quiz'))

@views.route('/pick-quiz', methods=['POST', 'GET'])
@login_required
def pick_quiz():
    if request.method == 'POST':
        global category
        global difficulty
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        global questions
        global answers
        questions, answers = fetcher(category, difficulty)
        return redirect(url_for('views.quiz'))
    return render_template('pick-quiz.html', user=current_user)

@views.route('/score', methods=['POST', 'GET'])
@login_required
def score():
    global answers
    global questions
    if answers != None and questions != None:
        questions_id = [i.id for i in questions]
        user_answers = [request.form.get(id) for id in questions_id]
        global category
        score = check_correct_answers(answers, user_answers)
        if request.method == 'POST':
            questions= None
            answers= None
        return render_template('score.html', user=current_user, score=score, category=category)
    else:
        return redirect(url_for('views.pick_quiz'))
