
    
from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from app.extensions import db
from app.setting import *
from app.models import *
from app.forms import *

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

    own_page = request.args.get('own_page', 1, type=int)
    liked_page = request.args.get('liked_page', 1, type=int)
    commented_page = request.args.get('commented_page', 1, type=int)

    # Query and paginate the user's own posts
    own_posts_pagination = Post.query.filter_by(author_id=user.id).order_by(Post.create_time.desc()).paginate(page=own_page, per_page=5, error_out=False)
    own_posts = own_posts_pagination.items

    # Query and paginate the posts liked by the user
    liked_posts_pagination = Post.query.join(Like, Post.id == Like.post_id).filter(Like.user_id == user.id).order_by(Post.create_time.desc()).paginate(page=liked_page, per_page=5, error_out=False)
    liked_posts = liked_posts_pagination.items

    # Query and paginate the posts commented on by the user
    commented_posts_pagination = Post.query.join(Comments, Post.id == Comments.post_id).filter(Comments.author_id == user.id).order_by(Post.create_time.desc()).paginate(page=commented_page, per_page=5, error_out=False)
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

        user.gender = request.form.get('gender')
        user.age = int(request.form.get('age', 0))
        user.mobile = request.form.get('mobile')
        user.email = request.form.get('email')
        user.signature = request.form.get('signature')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    return redirect(url_for('user.user'))