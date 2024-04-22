from flask import render_template, flash, redirect, url_for, request
from app import app
from app.login import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Questions
from werkzeug.urls import url_parse
from app import db
from app.login import RegistrationForm
from datetime import datetime

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():
    current_datetime = datetime.now()  # Get current local date and time

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'GET':
        questions = Questions.query.all()
        return render_template('form.html', questions=questions, current_datetime=current_datetime)  # Pass current_datetime to the template





def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'GET':
        questions = Questions.query.all()
        return render_template('form.html', questions=questions)
    
    for k, v in request.form.items():
        print(f"Incrementing {k}-{v}")
        question = Questions.query.get(k)
        
        curr = getattr(question, f"answers_option{v}", None)

        if not curr:
            curr = 0
        
        curr += 1
        setattr(question, f"answers_option{v}", curr)
    
    db.session.commit()
    return render_template('tak.html')
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
