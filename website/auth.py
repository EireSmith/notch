
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET' , 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user: 
            if check_password_hash(user.password, password):
                flash("logged in", category = "success")
                login_user(user, remember=True) #flask will remember user is logged in after system restart/disconnect
                return redirect(url_for("views.index")) 
            else:
                flash("incorrect password", category = "error")
        else: 
            flash("email does not exist", category = "error")
    
    return render_template('login.html', user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route('/signup', methods=['GET' ,'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash("email already exists", category = 'error')
        elif first_name == '' or family_name == '':
            flash('please enter full name',category='error')
        elif len(password) < 8:
            flash('password must be at least 8 characters', category='error')
        elif password != password_confirm:
            flash("passwords don't match", category='error')
        elif len(email) < 3:
            flash('enter valid email', category='error')
        else: 
            new_user = User(email = email, first_name = first_name, family_name = family_name, password = generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            
            flash('notch account created', category='success')

            return redirect(url_for("views.index"))
          
    return render_template('signup.html', user = current_user )