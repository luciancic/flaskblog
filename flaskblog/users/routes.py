import os
import secrets
from PIL import Image

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from flaskblog import db, bcrypt, mail
from flaskblog.forms import RegisterForm, LoginForm,\
                            UpdateAccountForm, RequestResetForm, PasswordResetForm
from flaskblog.models import User, Post


users = Blueprint('users', import_name=__name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(next_url) if next_url else redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account was created. You may now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def save_picture(picture_file):
    filename = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_file.filename)
    filename = filename + f_ext
    i_path = os.path.join(users.root_path, f'static/profile_pics/{filename}')
    print(picture_file.filename)
    i = Image.open(picture_file)
    i.thumbnail((100, 100))
    i.save(i_path)

    return filename


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info updated', 'success')
        return redirect(url_for('users.account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = os.path.join('static', 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)

@users.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    image_file = os.path.join('/', 'static', 'profile_pics', user.image_file)
    #pylint: disable=no-member
    pagination = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(per_page=4)
    return render_template('user.html', user=user, image_file=image_file, pagination=pagination)


@users.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        message = Message(subject='Reset Password - Flaskblog',
                          recipients=[user.email], sender=('Flaskblog', 'noreply@flaskblog.com'))
        message.body = f'''Click the link below to reset your password:
{url_for('users.password_reset', token=user.generate_user_token(), _external=True)}

If you did not request a password reset you can safely ignore this email.
'''
        mail.send(message)
        flash('An email has been sent with reset instructions.', 'info')
    return render_template('request_reset.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_user_token(token)
    if not user:
        flash('Token invalid or expired.', 'warning')
        return redirect('request_reset')
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password was reset. You may now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('password_reset.html', form=form)
