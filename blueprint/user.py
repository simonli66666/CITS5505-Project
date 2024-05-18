""" from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/')
@index_bp.route('/index/')
def index():
    return render_template('frontend/index.html') """
    
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

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
@login_required
def user():
    user = current_user
    page = request.args.get('page', 1, type=int)

    own_posts_pagination = Post.query.filter_by(author_id=user.id).order_by(Post.create_time.desc()).paginate(page=page, per_page=10, error_out=False)
    own_posts = own_posts_pagination.items

    liked_posts_pagination = Post.query.join(Like, Post.id == Like.post_id).filter(Like.user_id == user.id).order_by(Post.create_time.desc()).paginate(page=page, per_page=10, error_out=False)
    liked_posts = liked_posts_pagination.items

    commented_posts_pagination = Post.query.join(Comments, Post.id == Comments.post_id).filter(Comments.author_id == user.id).order_by(Post.create_time.desc()).paginate(page=page, per_page=10, error_out=False)
    commented_posts = commented_posts_pagination.items

    return render_template(
        'frontend/user.html', 
        own_posts=own_posts, 
        liked_posts=liked_posts, 
        commented_posts=commented_posts, 
        own_posts_pagination=own_posts_pagination, 
        liked_posts_pagination=liked_posts_pagination, 
        commented_posts_pagination=commented_posts_pagination
    )

@user_bp.route('/edit_user_info', methods=['POST','GET'])
@login_required
def edit_user_info():
    if request.method == 'POST':
        user = current_user
        try:
            user.gender = request.form.get('gender')
            user.age = int(request.form.get('age', 0))
            user.mobile = request.form.get('mobile')
            user.email = request.form.get('email')
            user.signature = request.form.get('signature')

            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Failed to update profile.', 'error')
            print("Error:", e)
    return redirect(url_for('user.user'))