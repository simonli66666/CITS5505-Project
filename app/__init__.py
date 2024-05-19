from flask import Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from app.extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.models import User, Post
from app.setting import DevelopmentConfig
from app.blueprint.auth import auth_bp
from app.blueprint.main import main_bp
from app.blueprint.post import post_bp
from app.blueprint.user import user_bp
from app.blueprint.error import error_bp

import click

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(DevelopmentConfig)
    
    app.config['SECRET_KEY'] = 'admin'
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(error_bp)


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
    
    def register_extensions(app: Flask):
        db.init_app(app)

    with app.app_context():
        db.create_all
    migrate = Migrate(app, db)
    register_extensions(app)


    return app