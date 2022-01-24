from flask import Blueprint, render_template, request, json, url_for, redirect, flash, session
from flask_login import login_user, login_required, current_user, logout_user
from app.models import Booking, Store
import datetime

# Blueprint Configuration
manager_bp = Blueprint(
    'manager_bp', __name__,
)

"""
Route to view bookings in a partcular store that the manager is in charge of 
"""
@manager_bp.route("/bookings/", methods=['GET', 'POST'])
@manager_bp.route("/bookings/<p>", methods=['GET', 'POST'])
def viewBookings(p=None):
    if not session["logged_in"]:
        return redirect(url_for('login_bp.login'))
    if session["status"] != "Manager":
        return render_template("home_bp.home")


    active=False
    if(p=="all"):
        active=True
        bookings = Booking.query.filter_by(store_id=current_user.store_id).order_by(Booking.bookingDate.desc())
    else:
        bookings = Booking.query.filter_by(store_id=current_user.store_id,bookingDate = datetime.date.today()).all()


    store=Store.query.filter_by(id=current_user.store_id).first()


    return render_template("manager/viewBookings.html",store=store, bookings = bookings,active=active)
