from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

 # 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# 用户模型定义
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# 确保在第一次请求时创建数据库表
@app.before_first_request
def create_tables():
    db.create_all()
    
# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 注册路由
@app.route('/register1', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            
            """ return render_template('index.html') """
            
            return render_template('index.html', error=True, username=username)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!','success')
        return redirect(url_for('login'))
    return render_template('index.html', error=False) 



# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Logged in successfully!')
            return render_template('login.html', user=user)  # Pass user data to login.html if needed
        else:
            flash('Invalid username or password!')
    return render_template('index.html')



 # 帖子详情页面
@app.route('/posts_details')
def posts_details():
    return render_template('postsDetails.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
    
    
"""     
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('logged_in'))
        flash('Invalid username or password')
    return render_template('index.html', form=form, login=True)  # Render index with login form

@app.route('/register1', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('logged_in'))
        flash('Username already exists.')
    return render_template('index.html', form=form, register=True)  # Render index with registration form

@app.route('/logged_in')
@login_required
def logged_in():
    return render_template('login.html')  # The page after login

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) """