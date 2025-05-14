from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager, login_user
import hashlib  # Import pour comparer les mots de passe hachés
from models import db, Users

login = Blueprint('login', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(login)

@login.route('/login', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Veuillez remplir tous les champs', 'error')
            return redirect(url_for('login.show'))

        user = Users.query.filter_by(email=email).first()

        if user:
            # Générer un hash du mot de passe saisi pour le comparer avec celui en base
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user.password == hashed_password:  # Comparaison directe
                login_user(user)
                flash('Connexion réussie', 'success')
                return redirect(url_for('home.show'))
            else:
                flash('Mot de passe incorrect', 'error')
                return redirect(url_for('login.show'))
        else:
            flash('Utilisateur introuvable', 'error')
            return redirect(url_for('login.show'))
    else:
        return render_template('login.html')

# Configuration additionnelle si nécessaire
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
