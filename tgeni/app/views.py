import flask
import app.forms    as forms
import app.models   as models

from app   import (tgeni, db, login_manager)
from flask import (Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import (login_required, login_user, logout_user, current_user)

@tgeni.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = models.User(username = request.form['username'],
                        email    = request.form['email'],
                        password = request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('New user registered')
    return redirect(url_for('index'))

@tgeni.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        # render the user login form
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    found_user = models.User.query.filter_by(username=username).first()
    if found_user and found_user.password_matches(password):
        login_user(found_user)
        flash('Logged in user')
        return redirect(url_for('index'))
    else:
        # username/password invalid
        flash('Invalid username or password', 'fail_login')
        return redirect(url_for('signin'))

@tgeni.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('home'))



@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))



@tgeni.errorhandler(400)
def fail_login(er):
    return '<h2>Oh no, 400!</h2>'

@tgeni.errorhandler(403)
def fail_login(er):
    return '<h2>Oh no, 403!</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'



@tgeni.route('/')
def home_():
    return redirect(url_for('home'))

@tgeni.route('/home')
def home():
    return render_template('home.html')


@tgeni.route('/index')
@login_required
def index():
    """ This view serves as the homepage for a signed-in user.
    """
    return render_template('index.html')

@tgeni.route('/add_trip', methods = ['GET', 'POST'])
@tgeni.route('/edit_trip/<trip_id>', methods = ['GET', 'POST'])
@login_required
def add_trip(trip_id=None):
    ######
    if trip_id:
        trip = models.Trip.query.get(trip_id)
        if trip:
            pass
            #if current_user not in trip.users:
                # Trip with this id exists but the logged-in user is
                #  not on it.
            #    return flask.abort(403)
            # else:
            #   Trip id exists and the logged-in user is on it.
        else:
            # No trip with this id exists!
            return flask.abort(400)
    else:
        # Trip id not provided, which means this is a new a trip.
        trip = models.Trip()
    ######
    form = forms.NewTripForm(obj=trip)
    if form.validate_on_submit(): # handles POST?
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_trip.html', form=form)

@tgeni.route('/view_trip', methods = ['GET', 'POST'])
@login_required
def view_trip():
    return render_template('view_trip.html')
