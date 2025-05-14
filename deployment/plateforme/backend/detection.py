from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from models import db, Users

detection = Blueprint('detection', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(detection)

@detection.route('/detection', methods=['GET'])
@login_required
def show():
    return render_template('detection.html')
