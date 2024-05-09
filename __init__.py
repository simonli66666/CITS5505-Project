from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from bbs.extensions import db
from bbs.models import *
from bbs.setting import *
import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user






# app = Flask('bbs')
app = Flask(__name__, static_folder='static')


app.config['SECRET_KEY'] = 'admin'

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('BBS_PER_PAGE', 10)
    pagination = Post.query.order_by(Post.update_time.desc()).paginate(page=page, per_page=per_page)
    latest = pagination.items
    return render_template('frontend/index.html', latest=latest, pagination=pagination)

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
            return render_template('frontend/index.html', error=True, username=username)
        if User.query.filter_by(nickname=nickname).first():
            flash('Username already exists!', 'error')
            return render_template('frontend/index.html', error=True, nickname=nickname)
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
            login_user(user)
        
            flash('Logged in successfully!', 'success')
            return redirect(url_for('recipes')) 
        else:
            flash('Invalid username or password!', 'error')
    return render_template('frontend/index.html')

# 发布菜单路由
@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
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
       
        
        post = Post(title=title,image=image, ingredient1=ingredient1,ingredient2=ingredient2, ingredient3=ingredient3, ingredient4=ingredient4, ingredient5=ingredient5, ingredient6=ingredient6,servings= servings, prep_time=prep_time, cooking_time=cooking_time, calories=calories, content=content, author_id=current_user.id )
        db.session.add(post)
        db.session.commit()
        flash('Recipt posted successfully!','success')
        return redirect(url_for('recipes', post_id=post.id))
    return render_template('frontend/login.html', error=False)

@app.route('/test')
def test():
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('frontend/test.html', posts=posts, pagination=pagination)

@app.route('/recipes')
@login_required
def recipes():
    return render_template('frontend/login.html')

@app.route('/user')
@login_required
def user():
    return render_template('frontend/user.html')

# 帖子详情页面
@app.route('/posts_details')
def posts_details():
    return render_template('frontend/postsDetails.html')



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
        click.confirm('这个操作会清空整个数据库,要继续吗?', abort=True)
        db.drop_all()
        click.echo('清空数据库完成!')
        db.create_all()
        click.echo('数据库初始化完成!')



register_error_handlers(app)
app.config.from_object(DevelopmentConfig)
register_extensions(app)
register_cmd(app)