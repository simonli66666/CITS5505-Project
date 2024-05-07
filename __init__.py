from flask import Flask, render_template, request, redirect, url_for, flash
from bbs.extensions import db
from bbs.models import *
from bbs.setting import *
import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user





def create_app(config_name=None):
    # app = Flask('bbs')
    app = Flask(__name__, static_folder='static')

    register_error_handlers(app)

    app.config['SECRET_KEY'] = 'admin'
    @app.route('/')
    def index():
        return render_template('frontend/index.html')
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'index'  # 未登录时重定向到的视图函数
    login_manager.login_message_category = 'info'
    # Flask-Login 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    # 注册路由
    @app.route('/register1', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            nickname = request.form['nickname']
            password = request.form['password']
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                
                """ return render_template('index.html') """
                
                return render_template('frontend/index.html', error=True, username=username)
            new_user = User(username=username,nickname=nickname, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!','success')
            return redirect(url_for('login'))
        return render_template('frontend/index.html', error=False) 



    # 登录路由
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                # login_user(user)
            
                flash('Logged in successfully!', 'success')
                return render_template('frontend/login.html')
            else:
                flash('Invalid username or password!', 'error')
        return render_template('frontend/index.html')


    
    @app.route('/recipes')
    @login_required
    def recipes():
        return render_template('frontend/login.html')
    
    # 帖子详情页面
    @app.route('/posts_details')
    def posts_details():
        return render_template('frontend/postsDetails.html')

   

    register_error_handlers(app)
    app.config.from_object(DevelopmentConfig)
    register_extensions(app)
    register_cmd(app)
    return app

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
        click.confirm('这个操作会清空整个数据库,要继续吗?', abort=True)
        db.drop_all()
        click.echo('清空数据库完成!')
        db.create_all()
        click.echo('数据库初始化完成!')