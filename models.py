from database import db


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    password = db.Column('password', db.String(255))
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(20))
    email = db.Column('email', db.String(30))
    passtype = db.Column('passtype', db.String(15))

    def __init__(self, password, first_name, last_name, email, passtype):
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.passtype = passtype


class Event(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    location = db.Column('location', db.String(50))
    time = db.Column('time', db.Integer)
    recurring = db.Column('recurring', db.String(10))

    def __init__(self, location, user_id, time, recurring):
        self.location = location
        self.user_id = user_id
        self.time = time
        self.recurring = recurring


class Deck(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    coord_x = db.Column('coord_x', db.Float)
    coord_y = db.Column('coord_y', db.Float)
    name = db.Column('name', db.String(30))
    commuter = db.Column('commuter', db.Boolean)
    resident = db.Column('resident', db.Boolean)
    staff = db.Column('staff', db.Boolean)
    percent = db.Column('percent', db.Integer)
    distance = db.Column('distance', db.Integer)

    def __init__(self, coord_x, coord_y, name, commuter, resident, staff, percent, distance):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.name = name
        self.commuter = commuter
        self.resident = resident
        self.staff = staff
        self.percent = percent
        self.distance = distance


class Building(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    coord_x = db.Column('coord_x', db.Float)
    coord_y = db.Column('coord_y', db.Float)
    name = db.Column('name', db.String(30))
    time = db.Column('time', db.String(255))

    def __init__(self, coord_x, coord_y, name, time):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.name = name
        self.time = time


class Capacity(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    percent = db.Column('coord_x', db.String(4))
    name = db.Column('name', db.String(30))

    def __init__(self, percent, name):
        self.percent = percent
        self.name = name
