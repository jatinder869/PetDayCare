from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date,timedelta

"""The file contains database tables for different entities in our project. They are basically SQL tables .
In different classes , we can also define getter/setter methods for any column required by controller
"""




"""
This is a class for every User in our database be it (Customer , Manager or Employee).

"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    customer = db.relationship('Customer', backref='user', uselist=False)
    employee = db.relationship('Employee', backref='user', uselist=False)
    manager = db.relationship('Manager', backref='user', uselist=False)

    def _repr_(self):
        return f"User( '{self.email}', '{self.pets}')"

    # the method first encrypts the given password and set it in the database
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )



    # the method checks if the given password matches the encrypted password in database
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_name(self):
        return self.full_name

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_address(self):
        return self.address

    def get_user(self):
        if self.status == "Customer":
            return self.customer
        elif self.status == "Employee":
            return self.employee
        else:
            return self.manager


"""This is a class for the customer table """
class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    bookings = db.relationship('Booking', backref='customer')
    subscriptionStartDay = db.Column(db.String(20), nullable=True)
    subscriptionEndDay = db.Column(db.String(20), nullable=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=True, default=-1)
    pets = db.relationship('Pet', backref='owner', lazy=True)
    cards = db.relationship('Card', backref='owner', lazy=True)



    # helps to set subscription start and end time by getting todays date and also the subscription duration
    def setSubscriptionTime(self):
        date_time=date.today()
        self.subscriptionStartDay=date_time
        self.subscriptionEndDay=date_time+timedelta(days=self.subscription.durationInWeeks*7)

    def update_phone(self, phone_num):
        self.user.phone = phone_num

    def update_address(self, address):
        self.user.address = address

    def update_name(self, name):
        self.user.name = name

    def get_pets(self):
        """Check hashed password."""
        return self.pets

    def get_cards(self):
        """Check hashed password."""
        return self.cards

    def get_name(self):
        return self.user.get_name()

    def get_email(self):
        return self.user.email

    def get_phone(self):
        return self.user.phone

    def get_address(self):
        return self.user.get_address()

    def repr(self):
        return f"User('{self.name}', '{self.email}', '{self.pets}')"

    def has_subscription(self):
        return self.subscription_id != -1

    def get_subscription(self):
        return self.subscription


"""Class for the pet table owned by a customer"""
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    instruction = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    booking = db.relationship('Booking', backref='pet')
    def repr(self):
        return f"Pet('{self.type}', '{self.name}')"

"""Class for the card table owned by a customer"""
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardnum = db.Column(db.String(20), unique=True)
    expiry = db.Column(db.Integer)
    name = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def getExpiry(self):
        expiry_str= str(self.expiry)
        if(len(expiry_str)==3):
            return "0"+expiry_str[0]+"/"+expiry_str[1:]
        else:
            return expiry_str[:2]+"/"+expiry_str[2:]



    def getNumber(self):
        credit_num=str(self.cardnum)
        return credit_num[0:4]+" "+credit_num[4:8]+" "+credit_num[8:12]+" "+credit_num[12:16]


    def _repr_(self):
        return f"Card('{self.cardnum}', '{self.name}')"

"""Class for the Employee table"""
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dayAvailable = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)

    def _repr_(self):
        return f"User('{self.name}', '{self.email}','{self.dayAvailable}')"

"""Class for the Manager table"""
class Manager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), unique=True)
    employees = db.relationship('Employee', backref='employee', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def _repr_(self):
        return f"User('{self.name}', '{self.email}')"

    def get_name(self):
        return self.user.get_name()

    def get_email(self):
        return self.user.email

    def get_phone(self):
        return self.user.phone

    def get_address(self):
        return self.user.get_address()

"""Class for the store table linked to a particular manager and a city"""
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(20), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    province = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    openTime = db.Column(db.String(4), nullable=False)
    closeTime = db.Column(db.String(4), nullable=False)
    curManager = db.relationship('Manager', backref='store', lazy=True)  # change backref to 'store'
    bookings = db.relationship('Booking', backref='store')
    lat=db.Column(db.String(20), nullable=False)
    lng=db.Column(db.String(20), nullable=False)

    def getCityName(self):
        return self.city.name;

    def __repr__(self):
        return f"Store('{self.street}','{self.city}','{self.province}')"

"""Class for the city table which also contains the list of all stores in the city"""
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    stores = db.relationship('Store', backref="city", lazy=True)

    def get_stores(self):
        return self.stores

"""Class for the booking table linked to a particular customer, store and pet"""
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.String(20), nullable=False)
    endTime = db.Column(db.String(20), nullable=False)
    bookingDate = db.Column(db.String(20), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), unique=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), unique=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), unique=False)
    instruction = db.Column(db.String(120), nullable=False)

"""Class for the Subscription table which contains reference to all the customers currently on the particularsubscription"""
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    durationInWeeks = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    priceInDollars = db.Column(db.Integer, nullable=False)
    customers = db.relationship('Customer', backref='subscription', lazy=True)
    description = db.Column(db.String(120), nullable=False)

