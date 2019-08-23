from flask import Blueprint, render_template

from flaskblog.models import Post


main = Blueprint('main', import_name=__name__)


@main.route('/')
def home():
    #pylint: disable=no-member
    pagination = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4)
    return render_template('home.html', pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
