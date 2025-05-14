from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from models import db, Users

classification2 = Blueprint('classification2', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(classification2)

@classification2.route('/classification2', methods=['GET'])
@login_required
def show():
    return render_template('classification2.html')
