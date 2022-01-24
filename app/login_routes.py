from flask import Blueprint, render_template, request, json, url_for, redirect, flash, session
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import LoginForm, RegistrationForm
from app import db
from app import login_manager

from app.models import User, Customer

# Blueprint Configuration
login_bp = Blueprint(
    'login_bp', __name__,
)


"""
Route for login purpose 
Presents form to the user -> Check credentials are correct -> Login and set the session
"""
@login_bp.route("/login/", methods=['GET', 'POST'])
@login_bp.route("/login/<rd>", methods=['GET', 'POST']) # rd param is for redirecting
def login(rd=None):
    if current_user.is_authenticated:
        return redirect(url_for('profile_bp.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):

            login_user(user)
            session["logged_in"] = True
            session["status"] = user.status


            if rd is not None:
                return redirect(url_for(rd))

            if user.status=="Customer":
                return redirect(url_for('profile_bp.dashboard'))
            elif user.status=="Manager":
                return redirect(url_for('manager_bp.viewBookings'))

        flash('Invalid username/password combination')
        return redirect(url_for('login_bp.login'))

    return render_template("login/login.html", form=form, rd=rd)


"""
Route for registering user 
Presents Registration Form to the user -> Validates form ->Check if user already exists -> Creates new user ->
Login and set the session
"""
@login_bp.route("/register/", methods=['GET', 'POST'])
@login_bp.route("/register/<rd>", methods=['GET', 'POST'])
def register(rd=None):
    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user is None:
            new_user = User(
                phone=request.form["phone"],
                full_name=request.form["full_name"],
                address=request.form["address"],
                email=request.form["email"],
                status="Customer"
            )

            new_user.set_password(request.form["password"])

            db.session.add(new_user)
            db.session.commit()
            customer = Customer(
                user_id=new_user.id
            )
            db.session.add(customer)
            db.session.commit()

            login_user(new_user)
            session["logged_in"] = True
            if rd is not None:
                return redirect(url_for(rd))
            return redirect(url_for("profile_bp.dashboard"))
        flash("User with email address or username already exists! ")

    return render_template("login/register.html", form=form)

"""
This is a function used by login manager
It returns the current user by using the user_id
"""
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        user = User.query.get(user_id)
        if user is not None:
            return user.get_user()
        else:
            print("User not found")
    return None

"""
Route for logout  
Delets the session variables used while logging in
"""
@login_bp.route("/logout")
# @login_required
def logout():
    logout_user()
    session["logged_in"] = False
    session["status"] = None
    return redirect(url_for('login_bp.login'))

"""
This function is loaded when the user is accessing the page which requires login but he/she is not logged in
"""
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login_bp.login'))
