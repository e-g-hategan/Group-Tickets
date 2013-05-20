from google.appengine.ext import db
import re, os
import json

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
    prices = db.StringProperty()

def user_key():
    """Constructs a Datastore key for User."""
    return db.Key.from_path('User', 'default')

def day_key():
    """Constructs a Datastore key for Day."""
    return db.Key.from_path('Day', 'default')

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
    None

def set_day_buyer(date, user_id):
    None

def set_day_user_schedule_type(date, user_id, schedule_type):
    None

def set_day_user_guests(date, user_id, number_of_guests):
    None

def get_day(date):
    items = db.GqlQuery("SELECT * "
                        "FROM Day  "
                        "WHERE ANCESTOR IS :1 AND date IS :2",
                        day_key,
                        date)
    if items.length == 0:
        return None
    else:
        item = items[0]
        return {
            'date': item.date,
            'price': item.price,
            'buyer': item.buyer,
            'users': json.loads(item.users),
            'guests': json.loads(item.guests)}
