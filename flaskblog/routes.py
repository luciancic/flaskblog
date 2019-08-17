import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterForm, LoginForm, UpdateAccountForm, CreatePostForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    posts = Post.query.all()
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


def save_picture(picture_file):
    filename = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_file.filename)
    filename = filename + f_ext
    i_path = os.path.join(app.root_path, f'static/profile_pics/{filename}')
    print(picture_file.filename)
    i = Image.open(picture_file)
    i.thumbnail((100, 100))
    i.save(i_path)

    return filename


@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = os.path.join('static', 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('post_new.html', title='New Post', legend='New Post', form=form)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('home'))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_update.html', title='New Post', legend='Update Post', form=form)


@app.route('/post/<int:post_id>/delete', methods=['GET', 'DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    image_file = os.path.join('/', 'static', 'profile_pics', user.image_file)
    return render_template('user.html', user=user, image_file=image_file)
