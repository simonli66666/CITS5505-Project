""" from flask import Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') """

from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from app.extensions import db
from app.setting import *
from app.models import *
from app.forms import *

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from alembic import op
import sqlalchemy as sa

from werkzeug.security import generate_password_hash, check_password_hash
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    login_form = LoginForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    if request.method == 'POST':
        if registration_form.validate_on_submit():
            username = registration_form.username.data
            nickname = registration_form.nickname.data
            password = registration_form.password.data 
            
            password = generate_password_hash(password)
            # 检查用户名和昵称是否已存在
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return render_template('frontend/index.html', error=True, registration_form=registration_form, login_form=login_form, posts=posts, pagination=pagination)
            if User.query.filter_by(nickname=nickname).first():
                flash('Nickname already exists!', 'error')
                return render_template('frontend/index.html', error=True, registration_form=registration_form, login_form=login_form, posts=posts, pagination=pagination)
            
        
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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))