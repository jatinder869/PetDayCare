from flask import Blueprint, render_template, request, json, flash, url_for, redirect, session
from flask_login import login_required, current_user
from app.forms import UserUpdateForm, PetForm, CardForm,AddSubForm
from app.models import User, Pet, Customer, Card, Subscription
from app import db, models

# Blueprint Configuration
profile_bp = Blueprint(
    'profile_bp', __name__, url_prefix="/profile"
)


@profile_bp.route("/", methods=['GET', 'POST'])
@profile_bp.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserUpdateForm()


    return render_template("profile/dashboard.html", form=form, user=current_user)

@profile_bp.route("/updateuser", methods=['GET', 'POST'])
@login_required
def updateuser():
    form = UserUpdateForm()

    if form.validate_on_submit():
        print("validated")
        print(request.form["phone"])
        current_user.update_phone(request.form["phone"])
        current_user.update_address(request.form["address"])
        current_user.update_name(request.form["full_name"])
        db.session.commit()
        flash("Updated Succesfully")
        return render_template("profile/dashboard.html", form=form, user=current_user)

    print(request.form["phone"])

    return render_template("profile/dashboard.html", form=form, user=current_user)



@profile_bp.route("/pets", methods=['GET', 'POST'])
@login_required
def pets():
    user_pets = current_user.get_pets()

    return render_template("profile/pets.html", pets=user_pets)


@profile_bp.route("/addpet", methods=['GET', 'POST'])
@login_required
def addpet():
    form = PetForm()
    if form.validate_on_submit():

        pet = Pet(
            name=form.name.data,
            type=form.type.data,
            instruction=form.instruction.data,
            owner_id=current_user.id
        )

        db.session.add(pet)
        db.session.commit()

        if request.args.get("rd"):
            return redirect(request.args.get("rd"))

        return redirect(url_for("profile_bp.pets"))

    return render_template("profile/addpets.html", form=form)


@profile_bp.route("/cards", methods=['GET', 'POST'])
@login_required
def cards():
    user_cards = current_user.get_cards()

    return render_template("profile/cards.html", cards=user_cards)


@profile_bp.route("/addcard", methods=['GET', 'POST'])
@login_required
def addcard():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(
            name=form.name.data,
            expiry=form.expiry.data,
            cardnum=form.cardnum.data,
            owner_id=current_user.id
        )

        db.session.add(card)
        db.session.commit()

        return redirect(url_for("profile_bp.cards"))

    return render_template("profile/addcards.html", form=form)


@profile_bp.route("/subscription", methods=['GET', 'POST'])
@login_required
def subscriptions():
    user_subscriptions = current_user.get_subscription()
    check_subs = current_user.has_subscription()
    return render_template("profile/subscription.html", subscription=user_subscriptions, check_sub=check_subs,
                           customer=current_user)


@profile_bp.route("/addsubscription", methods=['GET', 'POST'])
@login_required
def add_subscriptions():
    form=AddSubForm()
    cards=current_user.get_cards()
    allCards=[]
    for card in cards:
        allCards.append((card.id,card.name+" "+card.cardnum))

    form.creditcard.choices=allCards

    if request.form.get("sub_id"):

        id = request.form["sub_id"]


        current_user.subscription_id = id
        current_user.setSubscriptionTime()
        db.session.commit()
        return redirect(url_for("profile_bp.subscriptions"))
    else:


        return render_template("profile/addsubscription.html", subscriptions = Subscription.query.all(),form=form)
