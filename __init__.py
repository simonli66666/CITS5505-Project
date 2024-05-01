from flask import Flask, render_template

def create_app(config_name=None):
    app = Flask('bbs')
    app = Flask(__name__, static_folder='static')


    @app.route('/')
    def index():
        return render_template('frontend/index.html')
    
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
