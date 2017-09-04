from flask import render_template, flash, redirect, request, abort, url_for
from app import app, models, db
from .forms import LoginForm, is_safe_url, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = models.load_user(form.username.data)
        if user and user.is_correct_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You\'ve been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data,
                           password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering, Please Log In')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_required
@app.route('/myProfile')
def iprofile():
    return 'Secret!'
