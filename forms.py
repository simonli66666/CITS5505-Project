from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField, FileField, Label, HiddenField, \
    PasswordField
from wtforms.validators import DataRequired, Length, Regexp

class BaseUserForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(message='Username cannot be empty'),
                                        Length(min=1, max=16, message='Username must be between 1 and 16 characters long'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='Username can only contain letters, numbers, and underscores.')],
                            render_kw={'placeholder': 'Please enter a username between 1-16 characters'})
    nickname = StringField('Nickname',
                           validators=[DataRequired(message='Nickname cannot be empty'),
                                       Length(min=1, max=20, message='Nickname must be between 1 and 20 characters long')],
                           render_kw={'placeholder': 'Please enter a nickname between 1-20 characters'})
    
    submit = SubmitField('Register', render_kw={'class': 'btn btn-success btn-xs'})

class RegisterForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(message='Username cannot be empty'),
                                        Length(min=1, max=16, message='Username must be between 1-16 characters'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='Username can only contain letters, numbers, and underscores')],
                            render_kw={'placeholder': 'Enter a username (1-16 characters)'})
    nickname = StringField('Nickname',
                           validators=[DataRequired(message='Nickname cannot be empty'),
                                       Length(min=1, max=20, message='Nickname must be between 1-20 characters')],
                           render_kw={'placeholder': 'Enter a nickname (1-20 characters)'})
    password = StringField('Password',
                           validators=[DataRequired(message='Password cannot be empty'),
                                       Length(min=8, max=40, message='Password must be between 8-40 characters'),
                                       EqualTo('confirm_pwd', message='Passwords must match')],
                           render_kw={'placeholder': 'Enter password', 'type': 'password'})
    confirm_pwd = StringField('Confirm Password',
                              validators=[DataRequired(message='Confirmation cannot be empty'),
                                          Length(min=8, max=40, message='Password must be between 8-40 characters')],
                              render_kw={'placeholder': 'Confirm password', 'type': 'password'})
    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary btn-xs mt-2'})


    def validate_user_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already registered.')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('This nickname is already registered.')