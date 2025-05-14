from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager
import sqlalchemy
from werkzeug.security import generate_password_hash  # Still use Werkzeug for hash
import hashlib  # For SHA-256
from models import db, Users

register = Blueprint('register', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if not email.endswith('@gmail.com'):
                flash("Le domaine de l'email est non valide", 'error')
                return redirect(url_for('register.show'))
            if len(password) >= 8 and password == confirm_password:
                # Check if the user already exists
                existing_user = Users.query.filter_by(email=email).first()
                if existing_user:
                    flash('L\'utilisateur existe déjà', 'error')
                    return redirect(url_for('register.show'))

                # Hash the password using SHA-256
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                    flash('Compte bien créé', 'success')
                    return redirect(url_for('login.show'))
                except sqlalchemy.exc.IntegrityError:
                    flash('Une erreur s\'est produite lors de la création du compte', 'error')
                    return redirect(url_for('register.show'))
            else: 
                if len(password) < 8:
                    flash('La longueur minimale du mot de passe n\'est pas respectée', 'error')
                    return redirect(url_for('register.show'))
                else:
                    flash('Les mots de passe ne correspondent pas', 'error')
                    return redirect(url_for('register.show'))
        else:
            flash('Veuillez remplir tous les champs', 'error')
            return redirect(url_for('register.show'))
    else:
        return render_template('register.html')
