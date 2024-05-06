from flask import Flask, render_template
from bbs.extensions import db

from bbs.models import *




def create_app(config_name=None):
    # app = Flask('bbs')
    app = Flask(__name__, static_folder='static')

    register_error_handlers(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('frontend/index.html')
    
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
                
                return render_template('frontend/index.html', error=True, username=username)
            new_user = User(username=username, password=password)
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
                flash('Logged in successfully!')
                return render_template('frontend/login.html', user=user)  # Pass user data to login.html if needed
            else:
                flash('Invalid username or password!')
        return render_template('frontend/index.html')



    # 帖子详情页面
    @app.route('/posts_details')
    def posts_details():
        return render_template('frontend/postsDetails.html')

   

    register_error_handlers(app)

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


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080)



