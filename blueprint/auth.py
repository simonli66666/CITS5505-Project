""" from flask import Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') """

from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from bbs.extensions import db
from bbs.setting import *
from bbs.models import *
from bbs.forms import *

import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from alembic import op
import sqlalchemy as sa
from flask import g

from werkzeug.security import generate_password_hash, check_password_hash
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    login_form = LoginForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    if registration_form.validate_on_submit():
        username = registration_form.username.data
        nickname = registration_form.nickname.data
        password = registration_form.password.data 
        password = generate_password_hash(password)
        new_user = User(username=username, nickname=nickname, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('frontend/index.html', registration_form=registration_form, login_form=login_form, error=False, posts=posts, pagination=pagination)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=login_form.remember_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('post.recipes'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('frontend/index.html', login_form=login_form, registration_form=registration_form, posts=posts, pagination=pagination)