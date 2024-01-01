from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .models import Scores
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged In!', category='success')
                login_user(user, remember=remember_me)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password!', category='error')
        else:
            flash('Email Does Not Exist.', category='error')
        
    
    return render_template('login.html', user=current_user)


@auth.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':

        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Registered!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif password != password1:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, user_name=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            starting_scores = Scores(
                user_id=current_user.id, science_computers=0,mythology=0,sports=0,vehicles=0,general_knowledge=0,
                science_computers_medium=0,mythology_medium=0,sports_medium=0,vehicles_medium=0,general_knowledge_medium=0,
                science_computers_hard=0,mythology_hard=0,sports_hard=0,vehicles_hard=0,general_knowledge_hard=0
                )
            db.session.add(starting_scores)
            db.session.commit()
            flash('Account Created!', category='success')
            return redirect(url_for('views.profile'))

    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!', category='success')
    return redirect(url_for('views.home'))


@auth.route('/admin')
@login_required
def admin():
    admin_list = ['ivex@gmail.com']
    accounts = User.query.all()
    for i in accounts:
        print(i.user_name)
    if current_user.email not in admin_list:
        flash('You Are Not An Administrator!', category='error')
        return redirect(url_for('views.home'))
    return render_template('admin.html', user=current_user, accounts = accounts)