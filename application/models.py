from application import app, db
import flask
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class RawItem(db.Model):
    __tablename__ = 'raw_items'
    id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.Integer, unique=True)
    category = db.Column(db.String)
    colour = db.Column(db.String)
    size = db.Column(db.String)
    quantity = db.Column(db.Integer)

    def __init__(self, sku_id, category, colour, size, quantity):
        self.sku_id = sku_id
        self.category = category
        self.colour = colour
        self.size = size
        self.quantity = quantity

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'sku_id': self.sku_id,
            'category': self.category,
            'colour': self.colour,
            'size': self.size,
            'quantity': self.quantity
        }


class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
        }
