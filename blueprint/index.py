from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/')
@index_bp.route('/index/')
def index():
    return render_template('frontend/index.html')