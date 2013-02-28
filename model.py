from google.appengine.ext import db
import re, os

class User(db.Model):
    """Models the user."""
    user_id = db.StringProperty()
    nickname = db.StringProperty()

class Schedule(db.Model):
    """Models the travel preference for a user for a particular day."""
    date = db.DateProperty()
    user_id = db.StringProperty()
    schedule = db.StringProperty()
    buying_tickets = db.BooleanProperty()

class Price(db.Model):
    """Models the travel preference for a user for a particular day."""
    price = db.FloatProperty()
    people = db.IntegerProperty()
    since = db.DateProperty()
    until = db.DateProperty()

def user_key():
    """Constructs a Datastore key for User."""
    return db.Key.from_path('User', 'default')

def schedule_key():
    """Constructs a Datastore key for Schedule."""
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

def set_day_price
def set_day_buyer
def set_day_user_schedule_type
def set_day_user_guests

def get_day