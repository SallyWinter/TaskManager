from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db # type: ignore
from app.login import LoginForm, RegistrationForm # type: ignore
from app.forms import EventForm
from app.models import User, Event # type: ignore
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse 

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'GET':
        allUsers = User.query.all()
        allEvents = Event.query.all()
        eventForm = EventForm()
        eventForm.id.data = "-1"
        return render_template('calender.html', testing=allUsers, form=eventForm, testing2=allEvents)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
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

@app.route('/updateTask', methods=['POST'])
def update_task():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if current_user.admin == True:
        eventForm = EventForm()
        
        id = eventForm.id.data

        print("admin får dette:", vars(eventForm.eventname))

        event = Event.query.get(int(id))

        if eventForm.removeEvent.data == "remove":
            db.session.delete(event)
            db.session.commit()
        else:
            newStatus = eventForm.status.data
            newEventName = eventForm.eventname.data
            newEventDescription = eventForm.description.data

            event.status = newStatus
            event.name = newEventName
            event.description = newEventDescription 
            # de andre felter... (readonly for burgeren)
            db.session.commit()

    else:
        eventForm = EventForm()
        id = eventForm.id.data
        newStatus = eventForm.status.data
        event = Event.query.get(int(id))
        event.status = newStatus
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/addTask', methods=['POST'])
def add_task():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if current_user.admin != True:
        return redirect(url_for("index"))


    eventForm = EventForm()
    eventForm.validate()
    newEvent = Event(
        name=eventForm.eventname.data,
        description=eventForm.description.data,
        startDateTime=eventForm.startDate.data,
        endDateTime=eventForm.endDate.data,
        # users=eventForm.users.data,
        # admins=eventForm.admins.data,
    )
    db.session.add(newEvent)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/getevents', methods=['GET'])
def get_events():
    allEvents = Event.query.all()
    eventArray = []
    for event in allEvents:
        eventArray.append(event.as_calender_event())
    return jsonify(eventArray)