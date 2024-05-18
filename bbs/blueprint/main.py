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
main_bp = Blueprint('main', __name__)


# Route for the home page
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Instantiate registration and login forms
    registration_form = RegistrationForm()
    login_form = LoginForm()
    # Get the search query from the form if provided
    search_query = request.form.get('search_query', '')
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)

    # If there's a search query, filter posts by title, content, or user's nickname
    if search_query:
        pagination = Post.query.join(User).filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%'),
                User.nickname.ilike(f'%{search_query}%')
            )
        ).paginate(page=page, per_page=5, error_out=False)
    else:
        # Otherwise, display the most recent posts
        pagination = Post.query.order_by(Post.create_time.desc()).paginate(page=page, per_page=5, error_out=False)

    # Get the list of posts for the current page
    posts = pagination.items

    # If there are no posts matching the search query, display a flash message
    if search_query and not posts:
        flash('No results found for your search query.')

    # Query the top 5 posts ordered by score in descending order
    popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()
    return render_template('frontend/index.html', posts=posts, pagination=pagination, popular_posts=popular_posts, registration_form=registration_form, login_form=login_form, search_query=search_query)

@main_bp.route('/badges')
@login_required
def badges():
    return render_template('frontend/badges.html')
