from flask import Flask, render_template, request, redirect, url_for, flash, current_app, g, jsonify
from bbs.extensions import db
from bbs.setting import *
from bbs.models import *

import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from alembic import op
import sqlalchemy as sa
from flask import g






# app = Flask('bbs')
app = Flask(__name__, static_folder='static')


app.config['SECRET_KEY'] = 'admin'

@app.context_processor
def inject_popular_posts():
    popular_posts = Post.query.order_by(Post.score.desc()).limit(5).all()
    return dict(popular_posts=popular_posts)
# 主页路由
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '')
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
    return render_template('frontend/index.html', posts=posts, pagination=pagination, popular_posts=popular_posts, search_query=search_query)


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
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        password = request.form['password']
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('frontend/index.html', error=True, username=username, posts=posts, pagination=pagination)
        if User.query.filter_by(nickname=nickname).first():
            flash('Username already exists!', 'error')
            return render_template('frontend/index.html', error=True, nickname=nickname, posts=posts, pagination=pagination)
        new_user = User(username=username,nickname=nickname, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!','success')
        return redirect(url_for('login'))
    
    return render_template('frontend/index.html', error=False, posts=posts, pagination=pagination) 



# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
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
    return render_template('frontend/index.html', posts=posts, pagination=pagination)

# 发布菜单路由
@app.route('/share', methods=['GET', 'POST'])
def share():
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
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
    return render_template('frontend/login.html', error=False, posts=posts, pagination=pagination)

@app.route('/test')
def test():
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('frontend/test.html', posts=posts, pagination=pagination)

@app.route('/recipes', methods=['GET', 'POST'])
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





@app.route('/user')
@login_required
def user():
    user = current_user

    own_page = request.args.get('own_page', 1, type=int)
    liked_page = request.args.get('liked_page', 1, type=int)
    commented_page = request.args.get('commented_page', 1, type=int)

    own_posts_pagination = Post.query.filter_by(author_id=user.id).order_by(Post.create_time.desc()).paginate(page=own_page, per_page=5, error_out=False)
    own_posts = own_posts_pagination.items
    
    liked_posts_pagination = Post.query.join(Like, Post.id == Like.post_id).filter(Like.user_id == user.id).order_by(Post.create_time.desc()).paginate(page=liked_page, per_page=5, error_out=False)
    liked_posts = liked_posts_pagination.items
    
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

# 帖子详情页面
@app.route('/read/<post_id>/', methods=['GET'])
def read(post_id):
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    post = Post.query.get_or_404(post_id)
    post.read_times += 1  # 增加阅读次数
    db.session.commit()   # 提交数据库更改
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all() 

    return render_template('frontend/postsDetails.html',post=post,posts=posts, pagination=pagination, comments=comments)

@app.route('/read2/<post_id>/', methods=['GET'])
def read2(post_id):
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第一页
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    post = Post.query.get_or_404(post_id)
    post.read_times += 1  # 增加阅读次数
    db.session.commit()   # 提交数据库更改
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamps.desc()).all() 

    return render_template('frontend/postsDetails_notlogin.html', post=post, posts=posts, pagination=pagination, comments=comments)

@app.route('/like/<int:post_id>/', methods=['POST', 'GET'])
@login_required
def like(post_id):
    if request.method == 'POST':
        success, message, is_liked = post_like(post_id)
        return jsonify(success=success, message=message, isLiked=is_liked)
    elif request.method == 'GET':
        success, is_liked = is_post_liked(post_id)
        return jsonify(success=success, isLiked=is_liked)

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

def is_post_liked(post_id):
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    return True, bool(like)

@app.route('/edit-user-info',  methods=['POST','GET'])
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
    return redirect(url_for('user'))  # 重定向到用户资料页面

    
@app.route('/post-comment/', methods=['POST'])
@login_required
def post_comment():
    comment_content = request.form.get('commentContent')
    post_id = request.form.get('postId')

    post = Post.query.get_or_404(post_id)
    com = Comments(body=comment_content, post_id=post_id, author_id=current_user.id)
    
    # # 如果评论帖子用户与发帖用户不为同一人则发送消息通知
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
        click.confirm('这个操作会清空整个数据库,要继续吗?', abort=True)
        db.drop_all()
        click.echo('清空数据库完成!')
        db.create_all()
        click.echo('数据库初始化完成!')



register_error_handlers(app)
app.config.from_object(DevelopmentConfig)
register_extensions(app)
register_cmd(app)
migrate = Migrate(app, db)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
