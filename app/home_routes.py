from flask import Blueprint, render_template, session, request, flash, redirect, url_for,json
from flask import current_app as app
from app.models import db, User, Store, Booking, Pet,City
from flask_login import current_user
from app.forms import BookingForm
import datetime

""""Routes for home page"""



# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates/home',
    static_folder='static'
)


"""
Route used to render the home page
"""
# Index page
@home_bp.route("/")
def home():
    return render_template("home/index.html")

"""
Route used to render the about page
"""
# About page
@home_bp.route("/about")
def about():
    return render_template("home/about.html")

"""
Route used to display the stores in a particular city (passed by get request 'city')
"""
# Page to view store using city
@home_bp.route("/stores", methods=["GET"])
def stores():
    city = request.args.get("city")

    if city: # check if city is passed in get request
        city=city.lower()
        check_city = City.query.filter_by(name=city).first()
        if check_city: # check if the particular city exists in our database
            stores=check_city.get_stores()
        else:
            return redirect(url_for("main_bp.error", msg="No Stores in " + city))

    else:
        return redirect(url_for("main_bp.error", msg="You need to enter the city"))


    if len(stores) == 0: # check if there are stores in the city
        return redirect(url_for("main_bp.error", msg="No Stores in " + city))


    return render_template("stores/index.html", city=city, stores=stores)

"""
Route used to render the bookform page
We first make sure that user is logged in 
There are two ways to get to the bookform page
1.) By directly clicking on book an appoitnment button on the navbar ;  No get request is passed in this case
2.) By clicking on a particular store in the /stores page , in this case get request containing city and the store is passed
to this route. We set the given city and store by default in the bookform page 
"""

@home_bp.route("/bookform", methods=["GET", "POST"])
def bookForm():
    if not current_user.is_authenticated:
        flash("You need to login first to book form")
        return redirect(url_for("login_bp.login", rd="home_bp.bookForm"))

    cities=City.query.all()
    form = BookingForm()
    cityChoices=[]
    get_city=request.args.get("city")
    for city in cities:
        if get_city:
            if city.name==get_city:
                form.city.default=city.id
                form.process()

        cityChoices.append((city.id,city.name))

    form.city.choices=cityChoices


    pets= current_user.get_pets()
    petChoices=[]
    for pet in pets:
        petChoices.append((pet.id,pet.name.capitalize()))

    form.pet.choices=petChoices


    cards=current_user.get_cards()
    cardChoices=[]
    for card in cards:
        cardChoices.append((card.id, str(card.name)+" "+ str(card.cardnum)))

    print(cardChoices)

    current_url=request.script_root+request.full_path


    if form.validate_on_submit():
        new_booking = Booking(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                startTime=form.startTime.data,
                endTime=form.endtime.data,
                bookingDate=form.bookingDate.data,
                instruction=form.instruction.data,
                store_id=request.form["store"],
                pet_id=form.pet.data,
                customer_id=current_user.id
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for("home_bp.home"))



    store = None
    if (request.args.get("store")):
        store=request.args.get("store")


    return render_template("booking/booking.html", form=form,store=store,user=current_user,url=current_url,cards=cardChoices)

"""
Returns the stores in a particular city(given by the post request) in the json format
"""
@home_bp.route("/bookform/getstoresincity", methods=["GET", "POST"])
def getStores():
    id=request.form["city_id"]


    stores=City.query.filter_by(id=id).first().get_stores();

    stores_json=[]
    for store in stores:
        stores_json.append({"id":store.id,"address":store.street,"default":False})

    return json.dumps(stores_json)