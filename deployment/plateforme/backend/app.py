from flask import Flask
from flask_login import LoginManager
from models import db, Users
from index import index
from login import login
from logout import logout
from register import register
from home import home
from prediction import prediction
from detection import detection
from users import users
from access_denied import access_denied
from classification1 import classification1
from classification2 import classification2

app = Flask(__name__, static_folder='../frontend')
app.secret_key = '1a2b3c4d5e'

# ✅ FIX: Proper MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Data-Base123@localhost/login_database'

# Initialize DB and LoginManager
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.show'  # Optional: redirects unauthorized users

# ✅ Create tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(prediction)
app.register_blueprint(detection)
app.register_blueprint(users)
app.register_blueprint(access_denied)
app.register_blueprint(classification1)
app.register_blueprint(classification2)


# User loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
