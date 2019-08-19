from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', [Required(), Length(min=2, max=20)])
    email = StringField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', [Required(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please choose another.')


class LoginForm(FlaskForm):
    email = StringField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', [Required(), Length(min=2, max=20)])
    email = StringField('Email', [Required(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already in use. Please choose another.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use. Please choose another.')


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[Required(), Length(max=100)])
    content = TextAreaField('Content', validators=[Required()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', [Required(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No account exists with this email.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', [Required(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', [Required(), EqualTo('password')])
    submit = SubmitField('Reset Password')