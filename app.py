import os

import bcrypt
from flask import Flask, redirect, url_for, render_template, request, session
from database import db
from models import User as User
from models import Event as Event
from models import Deck as Deck
from forms import RegisterForm, LoginForm
import webscrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///propark_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MCEKDM8348'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
        if session.get('user'):
                return render_template("index.html", user=session['user'])

        else:
                return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        passtype = request.form['passtype']
        # create user model
        new_user = User(h_password, first_name, last_name, request.form['email'], passtype )
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('index'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('index'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))



# Route to display all decks with no filter to the user
@app.route('/decks/', methods=['GET', 'POST'])
def show_decks():
        # calls the webscrapper
        percent = webscrap.scrap()

        if request.method == 'POST':
                # gather data posted from form on decks.html
                deck_filter = request.form['filter']
                deck_passtype = request.form['passtype']

                # redirect user to filtered decks page
                return redirect(url_for('display_filtered_decks', filter=deck_filter, passtype=deck_passtype))
        else:
                # query and display all decks
                # retrieves all decks
                display_decks= db.session.query(Deck).all()

                # for loop to iterate through the decks
                # second for loops iterates through the number of decks
                for items in display_decks:
                    for i in range(len(percent)):
                        # this checks if which value scraped connected to which deck
                        if percent[i][0] == items.name:
                            # this sets the percent value in the database to the new value
                            items.percent = percent[i][1]
                # commits it to be later called by the database
                db.session.commit()
                if session.get('user'):
                        return render_template("decks.html", user=session['user'], decks=display_decks)
                else:
                        return render_template("decks.html", decks=display_decks)


# Route to show decks when users have selected a filter and pass type
@app.route('/decks/<filter>/<passtype>', methods=['GET', 'POST'])
def display_filtered_decks(filter, passtype):
        # calls the webscrapper
        percent = webscrap.scrap()

        # if user submits a filter from form
        if request.method == 'POST':
                # recieve form data
                deck_filter = request.form['filter']
                deck_passtype = request.form['passtype']

                # restart display_filtered_decks with new filter
                return redirect(url_for('display_filtered_decks', filter=deck_filter, passtype=deck_passtype))

        else:
                # check passtype param and get decks matching it
                if passtype == "commuter":
                        filtered_decks = db.session.query(Deck).filter_by(commuter=True)
                elif passtype == "resident":
                        filtered_decks = db.session.query(Deck).filter_by(resident=True)
                elif passtype == 'faculty':
                        filtered_decks = db.session.query(Deck).filter_by(staff=True)
                else:
                        filtered_decks = db.session.query(Deck).all()

        # for loop to iterate through the decks
        # second for loops iterates through the number of decks
        for items in filtered_decks:
            for i in range(len(percent)):
                # this checks if which value scraped connected to which deck
                if percent[i][0] == items.name:
                    # this sets the percent value in the database to the new value
                    items.percent = percent[i][1]
        # commits it to be later called by the database
        db.session.commit()

        # if a user is logged in, render decks.html with user and decks
        if session.get('user'):
                return render_template('decks.html', decks=filtered_decks, user=session['user'], filter=filter, passtype=passtype)

        # if no user is logged in, render decks.html with decks
        else:
                return render_template('decks.html', decks=filtered_decks, filter=filter, passtype=passtype)

@app.route('/schedule')
def display_schedule():
        if session.get('user'):
            my_events = db.session.query(Event).filter_by(user_id=session['user_id'])
            return render_template("schedule.html", user=session['user'], event=my_events, user_id=session['user_id'])
        else:
            return render_template("schedule.html")

@app.route('/schedule/<event_id>', methods=['GET'])
def get_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        return render_template('building.html', event=my_event, user=session['user'])


@app.route('/schedule/create', methods=['GET', 'POST'])
def create():
        if session.get('user'):
            #form = ScheduleForm()
            if request.method == 'GET':
                return render_template('create.html', user=session['user'])

            if request.method == 'POST':
                location = request.form['location']
                time = request.form['time']
                event = Event(location, session['user_id'], time, 0)
                db.session.add(event)
                db.session.commit()
                return redirect('/schedule')
            else:
                return render_template("create.html")

        else:
            return redirect('/schedule')

@app.route('/schedule/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if request.method == 'POST':
        location = request.form['location']
        time = request.form['time']
        event = db.session.query(Event).filter_by(id=event_id).one()

        event.location=location
        event.time=time

        db.session.add(event)
        db.session.commit()

        return redirect('/schedule')
    else:
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        return render_template('create.html', event=my_event)

@app.route('/schedule/delete/<event_id>', methods=['POST'])
def delete_event(event_id):
    my_event = db.session.query(Event).filter_by(id=event_id).one()
    db.session.delete(my_event)
    db.session.commit()

    return redirect('/schedule')

@app.route('/settings', methods=['GET'])
def display_settings():
        if session.get('user'):
                return render_template("settings.html", user=session['user'])
        else:
                return render_template("settings.html")


if __name__ == "__main__":
    app.run()