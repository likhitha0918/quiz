import requests
import json
from random import choice

class Question():
    def __init__(self, question, option_1, option_2, option_3, option_4, id):
        self.question = question
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.id = id


def fetcher(category, difficulty):
    categories_dict = {
    'science_computers': '18',
    'general_knowledge': '9',
    'mythology': '20',
    'vehicles': '28',
    'sports': '21'
    }
    
    selected_category = categories_dict[category]
    selected_difficulty = difficulty

    url = f'https://opentdb.com/api.php?amount=10&category={selected_category}&difficulty={selected_difficulty}&type=multiple'
    request= requests.get(url)

    request_json = request.text

    res= json.loads(request_json)['results']
    id = 1
    questions_list = []
    question_answers = []
    for _ in res:
        current_question = _['question']
        current_question_answer = _['correct_answer']
        current_question_choices = [k for k in _['incorrect_answers']]
        current_question_choices.append(current_question_answer)
        
        opt_1 = choice(current_question_choices)
        current_question_choices.remove(opt_1)
        opt_2 = choice(current_question_choices)
        current_question_choices.remove(opt_2)
        opt_3 = choice(current_question_choices)
        current_question_choices.remove(opt_3)
        opt_4 = choice(current_question_choices)
        current_question_choices.remove(opt_4)
        
        
        question = Question(current_question, opt_1, opt_2, opt_3, opt_4, f'question{id}')

        question_answers.append(current_question_answer)
        questions_list.append(question)
        id+=1
    
    return questions_list, question_answers


def check_correct_answers(correct_answers,user_answers):
    score = 0
    for usr in user_answers:
        if usr in correct_answers:
            score +=1
    
    return score