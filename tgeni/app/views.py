import flask
import app.models as models

from app   import (tgeni, db, login_manager)
from flask import (Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import (login_required, login_user, logout_user)


@tgeni.route('/')
def home():
    return redirect(url_for('index'))

@tgeni.route('/index')
def index():
    return render_template('index.html')


@tgeni.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return Response('''
            <h1>Please enter your registration credentials:</h1>
            <form action="" method="post">
                <p><input type=text      name=username placeholder="username"></p>
                <p><input type=text      name=email    placeholder="email"></p>
                <p><input type=password  name=password placeholder="password"></p>
                <p><input type=submit    value="Register"></p>
            </form>
            ''')

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
        return Response('''
            <h1>Please enter your login credentials:</h1>
            <form action="" method="post">
                <p><input type=text      name=username placeholder="username"></p>
                <p><input type=password  name=password placeholder="password"></p>
                <p><input type=submit    value="Sign In"></p>
            </form>
            ''')

    username = request.form['username']
    password = request.form['password']
    found_user = models.User.query.filter_by(username=username).first()

    if found_user and found_user.password_matches(password):
        login_user(found_user)
        flash('Logged in user')
        return redirect(url_for('index'))
    else:
        # username/password invalid
        flash('Invalid username or password')
        return redirect(url_for('signin'))

@tgeni.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>Login failed.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'
