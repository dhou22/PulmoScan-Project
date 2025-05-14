from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from models import db, Users

access_denied= Blueprint('access_denied', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(access_denied)

@access_denied.route('/access_denied', methods=['GET'])
@login_required
def show():
    return render_template('access_denied.html')
