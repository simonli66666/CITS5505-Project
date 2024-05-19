"""from flask import Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from bbs.extensions import db
from bbs.setting import *
from bbs.models import *
from .forms import *

import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from alembic import op
import sqlalchemy as sa
from flask import g

from werkzeug.security import generate_password_hash, check_password_hash





# app = Flask('bbs')
app = Flask(__name__, static_folder='static')


app.config['SECRET_KEY'] = 'admin'

@app.context_processor
def inject_popular_posts():
    # Query the top 5 posts ordered by score in descending order
    popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()
    return dict(popular_posts=popular_posts)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
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

# Initialize the LoginManager for handling user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'index'  # Redirect to the home page if the user is not logged in
login_manager.login_message_category = 'info'

# Flask-Login user loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Instantiate registration and login forms
    registration_form = RegistrationForm()
    login_form = LoginForm()
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    # If the registration form is submitted and validated
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        nickname = registration_form.nickname.data
        password = registration_form.password.data 
        password = generate_password_hash(password)
        # Create a new user and save to the database
        new_user = User(username=username, nickname=nickname, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('frontend/index.html', registration_form=registration_form, login_form=login_form, error=False, posts=posts, pagination=pagination)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Instantiate login and registration forms
    login_form = LoginForm()
    registration_form = RegistrationForm()
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    # If the login form is submitted and validated
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=login_form.remember_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('recipes'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('frontend/index.html', login_form=login_form, registration_form=registration_form, posts=posts, pagination=pagination)

# Route for sharing recipes
@app.route('/share', methods=['GET', 'POST'])
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


@app.route('/test')
def test():
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    # Query and paginate posts, ordered by descending post ID
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('frontend/test.html', posts=posts, pagination=pagination)

@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    # Get the search query from the form if it's a POST request, otherwise from the URL
    search_query = request.form.get('search_query', '') if request.method == 'POST' else request.args.get('search_query', '')
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

    posts = pagination.items

    # If there are no posts matching the search query, display a flash message
    if search_query and not posts:
        flash('No results found for your search query.')

    # Query the top 5 posts ordered by score in descending order
    popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()

    return render_template('frontend/login.html', posts=posts, pagination=pagination, popular_posts=popular_posts, search_query=search_query)

@app.route('/user')
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

# Route for post details page
@app.route('/read/<post_id>/', methods=['GET'])
def read(post_id):
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    # Query and paginate posts, ordered by descending post ID
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    # Query the post by ID, return 404 if not found
    post = Post.query.get_or_404(post_id)
    post.read_times += 1  # Increment read times
    db.session.commit()   # Commit the change to the database
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all()

    return render_template('frontend/postsDetails.html', post=post, posts=posts, pagination=pagination, comments=comments)

@app.route('/read2/<post_id>/', methods=['GET'])
def read2(post_id):
    registration_form = RegistrationForm()
    login_form = LoginForm()
    # Get the current page number, default to 1
    page = request.args.get('page', 1, type=int)
    # Query and paginate posts, ordered by descending post ID
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    # Query the post by ID, return 404 if not found
    post = Post.query.get_or_404(post_id)
    post.read_times += 1  # Increment read times
    db.session.commit()   # Commit the change to the database
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all()

    return render_template('frontend/postsDetails_notlogin.html', post=post, posts=posts, pagination=pagination, comments=comments,registration_form=registration_form, login_form=login_form)

@app.route('/like/<int:post_id>/', methods=['POST', 'GET'])
@login_required
def like(post_id):
    # Like or unlike a post and return the result as JSON
    if request.method == 'POST':
        success, message, is_liked = post_like(post_id)
        return jsonify(success=success, message=message, isLiked=is_liked)
    elif request.method == 'GET':
        success, is_liked = is_post_liked(post_id)
        return jsonify(success=success, isLiked=is_liked)

def post_like(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if the user has already liked the post
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

def is_post_liked(post_id):
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    return True, bool(like)


@app.route('/edit-user-info', methods=['POST','GET'])
@login_required
def edit_user_info():
    if request.method == 'POST':
        user = current_user
        try:
            # Update user information from form data
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
    return redirect(url_for('user'))  # Redirect to user profile page

@app.route('/post-comment/', methods=['POST'])
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

@app.route('/badges')
@login_required
def badges():
    return render_template('frontend/badges.html')

def register_error_handlers(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500

def register_extensions(app: Flask):
    db.init_app(app)

def register_cmd(app: Flask):
    @app.cli.command()
    def admin():
        click.confirm('This operation will clear the entire database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Database cleared!')
        db.create_all()
        click.echo('Database initialized!')

# Register error handlers
register_error_handlers(app)
app.config.from_object(DevelopmentConfig)
# Register extensions
register_extensions(app)
# Register command-line commands
register_cmd(app)
# Initialize the migration tool
migrate = Migrate(app, db)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
"""

from flask import Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from bbs.extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bbs.models import User, Post
from bbs.setting import DevelopmentConfig
from bbs.blueprint.auth import auth_bp
from bbs.blueprint.main import main_bp
from bbs.blueprint.post import post_bp
from bbs.blueprint.user import user_bp
import click

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    app.config['SECRET_KEY'] = 'admin'
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(user_bp)

    @app.context_processor
    def inject_popular_posts():
        popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()
        return dict(popular_posts=popular_posts)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_error_handlers(app)
    register_cmd(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500

def register_cmd(app):
    @app.cli.command()
    def admin():
        click.confirm('This operation will clear the entire database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Database cleared!')
        db.create_all()
        click.echo('Database initialized!')

