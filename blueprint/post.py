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

post_bp = Blueprint('post', __name__)

@post_bp.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    search_query = request.form.get('search_query', '') if request.method == 'POST' else request.args.get('search_query', '')
    page = request.args.get('page', 1, type=int)

    if search_query:
        pagination = Post.query.join(User).filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%'),
                User.nickname.ilike(f'%{search_query}%')
            )
        ).paginate(page=page, per_page=5, error_out=False)
    else:
        pagination = Post.query.order_by(Post.create_time.desc()).paginate(page=page, per_page=5, error_out=False)

    posts = pagination.items

    if search_query and not posts:
        flash('No results found for your search query.')

    popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()

    return render_template('frontend/login.html', posts=posts, pagination=pagination, popular_posts=popular_posts, search_query=search_query)

# Route for sharing recipes
@post_bp.route('/share', methods=['GET', 'POST'])
def share():
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        image = request.form['image']
        ingredient1 = request.form['ingredient1']
        ingredient2 = request.form['ingredient2']
        ingredient3 = request.form['ingredient3']
        ingredient4 = request.form['ingredient4']
        ingredient5 = request.form['ingredient5']
        ingredient6 = request.form['ingredient6']
        servings = request.form['servings']
        prep_time = request.form['prep_time']
        cooking_time = request.form['cooking_time']
        calories = request.form['calories']
        content = request.form['content']
        
        # Create a new post and save to the database
        post = Post(
            title=title, image=image, ingredient1=ingredient1, ingredient2=ingredient2,
            ingredient3=ingredient3, ingredient4=ingredient4, ingredient5=ingredient5,
            ingredient6=ingredient6, servings=servings, prep_time=prep_time,
            cooking_time=cooking_time, calories=calories, content=content,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Recipe posted successfully!', 'success')
        return redirect(url_for('recipes', post_id=post.id))

    return render_template('frontend/login.html', error=False, posts=posts, pagination=pagination)

@post_bp.route('/read/<post_id>/', methods=['GET'])
def read(post_id):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    post = Post.query.get_or_404(post_id)
    post.read_times += 1
    db.session.commit()
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all()

    return render_template('frontend/postsDetails.html', post=post, posts=posts, pagination=pagination, comments=comments)

@post_bp.route('/read2/<post_id>/', methods=['GET'])
def read2(post_id):
    registration_form = RegistrationForm()
    login_form = LoginForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    post = Post.query.get_or_404(post_id)
    post.read_times += 1
    db.session.commit()
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all()
    return render_template('frontend/postsDetails_notlogin.html', post=post, posts=posts, pagination=pagination, comments=comments, registration_form=registration_form, login_form=login_form)

@post_bp.route('/like/<int:post_id>/', methods=['POST'])
@login_required
def like(post_id):
    success, message, is_liked = post_like(post_id)
    return jsonify(success=success, message=message, isLiked=is_liked)

def post_like(post_id):
    post = Post.query.get_or_404(post_id)
    c = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if c:
        post.likes_num -= 1
        db.session.delete(c)
        db.session.commit()
        return True, "You have unliked the post.", False
    else:
        post.likes_num += 1
        c = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(c)
        db.session.commit()
        return True, "You have liked the post.", True

@post_bp.route('/post-comment/', methods=['POST'])
@login_required
def post_comment():
    comment_content = request.form.get('commentContent')
    post_id = request.form.get('postId')

    post = Post.query.get_or_404(post_id)
    com = Comments(body=comment_content, post_id=post_id, author_id=current_user.id)
    
    # If the commenting user and the post author are different, send a notification
    # if current_user.id != post.author_id:
    #     notice = Notification(target_id=post_id, target_name=post.title, send_user=current_user.username,
    #                           receive_id=post.author_id, msg=comment_content)
    #     db.session.add(notice)
    
    post.update_time = datetime.datetime.now()
    db.session.add(com)
    db.session.commit()

    return jsonify({'tag': 1})