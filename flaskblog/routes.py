from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterForm, LoginForm
from flaskblog.posts_tmp import posts
from flaskblog.models import User
from flask_login import login_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Email not found', 'danger')
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Password incorrect', 'danger')
        else:
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {user.username}', 'success')
            next_url = request.args.get('next')
            return redirect(next_url) if next_url else redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You account was created. You may now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
