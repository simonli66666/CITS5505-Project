from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(400)
def bad_request(e):
    return render_template('error/400.html'), 400

@error_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403

@error_bp.app_errorhandler(404)
def not_found(e):
    return render_template('error/404.html'), 404

@error_bp.app_errorhandler(500)
def server_error(e):
    return render_template('error/500.html'), 500