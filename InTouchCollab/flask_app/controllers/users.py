from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.group import Group
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#**************************************
#   Home
#**************************************
@app.route("/")
def index():
    return render_template('index.html')

#**************************************
#   Login
#**************************************
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login_user", methods=["POST"])
def login_user():
    data = {
        'email' : request.form['email'],
    }
    user = User.get_user_by_email(data)

    #if email is not found
    if not user:
        flash('Invalid credentials')
        return redirect('/')

    # id password does not match
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid credentials')
        return redirect('/')

    # set id to session
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    flash('You successfully logged in')
    return redirect('/dashboard')

#**************************************
#   Register
#**************************************
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register_user", methods=["POST"])
def register_user():

    # validate input
    # if not User.validate_registration(request.form):
    #     return redirect('/')

    # hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    pw_verify_hash = bcrypt.generate_password_hash(request.form['confirm_password'])
    print(pw_hash)
    # add address to address table
    address_data = {
        # address
        "street1": request.form['street1'],
        "street2": request.form['street2'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zipcode": request.form['zipcode'],
        "country": request.form['country'],
    }

    address_id = User.add_address(address_data)

    user_data = {
        # user info
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "pw_verify" : pw_verify_hash,
        "phone": request.form['phone'],
        "phone_alt": request.form['phone_alt'],
        "address_id" : address_id
    }
    #if email already exists
    if User.get_user_by_email(user_data):
        flash('User with this email already exists')
        return redirect('/dashboard')

    # Call the save method on User
    user_id = User.save_user(user_data)
    user = User.get_user_by_email(user_data)
    # store user id into session
    session['user_id'] = user_id
    session['first_name'] = user.first_name

    flash('You successfully registered')
    return redirect("/dashboard")

#**************************************
#   Dashboard
#**************************************
@app.route("/dashboard")
def render_dashboard():

    groups = Group.get_all_groups()
    return render_template('dashboard.html', groups=groups)

#**************************************
#   Show a user
#**************************************
@app.route("/user/<int:id>")
def show_user(id):
    data = {
        'id':id, 
    }
    user = User.get_one(data)
    user['address'] = User.get_address(user)
    news = User.get_news(user['address'])
    groups = Group.getby_user(data)

    return render_template('show_user.html', user=user, news=news, groups = groups)