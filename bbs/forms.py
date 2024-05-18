from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import User  

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_nickname(self, nickname):
        user = User.query.filter_by(nickname=nickname.data).first()
        if user:
            raise ValidationError('Nickname already exists!')
        
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=25)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')