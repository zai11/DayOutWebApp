from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_user, login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from .forms import LoginForm,RegisterForm
from .models import User
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('nextp') #this gives the url from where the login page was accessed
            if nextp is None or not nextp.startswith('/'):
                flash('You have successfully logged in', 'success')
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            phone = register.phone_number.data
            uaddress = register.address.data
            isadmin = register.is_admin.data

            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists')
                return redirect(url_for('auth.register'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            print(isadmin)
            new_user = User(name=uname, emailid=email, phone_number=phone, address=uaddress, password_hash=pwd_hash, is_admin=isadmin)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')

@bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    nextp = request.args.get('nextp') #this gives the url from where the login page was accessed
    print(nextp)
    if nextp is None or not nextp.startswith('/'):
        flash('You are now logged out', 'warning')
        return redirect(url_for('main.index'))
    return redirect(nextp)