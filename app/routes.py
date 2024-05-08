from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User
from . import db
from app.models import Recipe

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/index1')
def index1():
    return render_template('index.html')

# 注册路由
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('index.html', error=True, username=username)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('routes.login'))
    return render_template('index.html', error=False)



# 登录路由
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)  # 使用 Flask-Login 登录用户
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.recipes'))  # 重定向到登录后页面
        else:
            flash('Invalid username or password!', 'error')
    return render_template('index.html')


# 注销路由
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('routes.login'))

# 需要登录的受保护页面
@bp.route('/badges')
@login_required
def badges():
    return render_template('Badges.html')

@bp.route('/postsDetails_notlogin')
@login_required
def postsDetails_notlogin():
    return render_template('postsDetails_notlogin.html')

@bp.route('/recipes')
@login_required
def recipes():
    return render_template('login.html')

@bp.route('/user_profile')
@login_required
def user_profile():
    return render_template('user.html')

@bp.route('/postsDetails')
@login_required
def postsDetails():
    return render_template('postsDetails.html')

@bp.route('/share_recipe', methods=['GET', 'POST'])
@login_required
def share_recipe():
    if request.method == 'POST':
        title = request.form['title']
        image_url = request.form['image_url']
        servings = request.form['servings']
        prep_time = request.form['prep_time']
        cooking_time = request.form['cooking_time']
        calories = request.form['calories']
        ingredient1 = request.form['ingredient1']
        ingredient2 = request.form['ingredient2']
        ingredient3 = request.form['ingredient3']
        ingredient4 = request.form['ingredient4']
        ingredient5 = request.form['ingredient5']
        ingredient6 = request.form['ingredient6']
        content = request.form['content']

        # 创建新的菜单实例
        new_recipe = Recipe(
            title=title,
            image_url=image_url,
            servings=servings,
            prep_time=prep_time,
            cooking_time=cooking_time,
            calories=calories,
            content=content,
            user_id=current_user.id
        )

        # 添加食材信息
        ingredients = ', '.join(filter(None, [ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6]))
        new_recipe.content = ingredients + '\n' + content

        # 保存到数据库
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe shared successfully!', 'success')
        return redirect(url_for('routes.recipe_details', recipe_id=new_recipe.id))

    return render_template('postDetails.html')

