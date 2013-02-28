from google.appengine.ext import db
import re, os

class User(db.Model):
    """Models the user."""
    user_id = db.StringProperty()
    nickname = db.StringProperty()

class Day(db.Model):
    """Models the travel preference for a user for a particular day."""
    date = db.DateProperty()
    price = db.FloatProperty()
    buyer = db.StringProperty()
    users = db.StringProperty()
    guests = db.StringProperty()

class Price(db.Model):
    """Models the travel preference for a user for a particular day."""
    since = db.DateProperty()
    prices = db.FloatProperty()

def user_key():
    """Constructs a Datastore key for User."""
    return db.Key.from_path('User', 'default')

def day_key():
    """Constructs a Datastore key for Day."""
    return db.Key.from_path('Schedule', 'default')

def price_key():
    """Constructs a Datastore key for Price."""
    return db.Key.from_path('Price', 'default')

def clean_model(model, model_key):
    items = db.GqlQuery("SELECT * "
                        "FROM " + model + " "
                        "WHERE ANCESTOR IS :1 ",
                        model_key)
    for item in items:
        item.delete()

def set_day_price(date, user_id, price):
def set_day_buyer(date, user_id):
def set_day_user_schedule_type(date, user_id, schedule_type):
def set_day_user_guests(date, user_id, number_of_guests):

def get_day(date):
    {
        'date': date,
        'price': 23.4,
        'buyer': 'george@swiftkey.net',
        'users': {
            'marek@swiftkey.net': 'Norm',
            'george@swiftkey.net': 'Late',
            'caroline@swiftkey.net': 'No'},
        'guests': {
            'george@swiftkey.net': 3}}