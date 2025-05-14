from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Users

users = Blueprint('users', __name__)

# Show all users (only for authorized admin)
@users.route('/users')
@login_required
def show():
    if current_user.email == 'nouha.aouachri@gmail.com':
        users_list = Users.query.all()
        return render_template('users.html', users=users_list)
    else:
        return render_template('access_denied.html')

# Add new user
@users.route('/users/add', methods=['POST'])
@login_required
def add():
    if current_user.email != 'nouha.aouachri@gmail.com':
        return render_template('access_denied.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash("All fields are required!", "danger")
        return redirect(url_for('users.show'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = Users(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully!", "success")
    return redirect(url_for('users.show'))

# Edit user
@users.route('/users/edit/<int:userid>', methods=['POST'])
@login_required
def edit(userid):
    if current_user.email != 'nouha.aouachri@gmail.com':
        return render_template('access_denied.html')

    user = Users.query.get_or_404(userid)

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash("All fields are required!", "danger")
        return redirect(url_for('users.show'))

    user.username = username
    user.email = email
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    db.session.commit()

    flash("User updated successfully!", "success")
    return redirect(url_for('users.show'))

# Delete user
@users.route('/users/delete/<int:userid>', methods=['POST'])
@login_required
def delete(userid):
    if current_user.email != 'nouha.aouachri@gmail.com':
        return render_template('access_denied.html')

    user = Users.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully!", "success")
    return redirect(url_for('users.show'))
