from application import app, db
import flask
from werkzeug.security import generate_password_hash, check_password_hash

import datetime


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


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    name = db.Column(db.String)
    lead_time = db.Column(db.String)

    def __init__(self, id, location, name, lead_time):
        self.id = id
        self.location = location
        self.name = name
        self.lead_time = lead_time

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'location': self.location,
            'name': self.name,
            'lead_time': self.lead_time,
        }


class IncomingProduct(db.Model):
    __tablename__ = 'incoming_products'
    id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.Integer, unique=True)
    location = db.Column(db.String)
    reorder_point = db.Column(db.Integer)
    demand = db.Column(db.Integer)
    total_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, sku_id, location, reorder_point, demand, total_quantity, updated_at=None):
        self.sku_id = sku_id
        self.location = location
        self.reorder_point = reorder_point
        self.demand = demand
        self.total_quantity = total_quantity
        self.updated_at = updated_at or datetime.datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'sku_id': self.sku_id,
            'location': self.location,
            'reorder_point': self.reorder_point,
            'demand': self.demand,
            'total_quantity': self.total_quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class PlainClothing(db.Model):
    __tablename__ = 'plain_clothing'
    id = db.Column(db.Integer, primary_key=True)
    incoming_product_id = db.Column(
        db.Integer, db.ForeignKey('incoming_products.id'), unique=True)
    incoming_product_sku_id = db.Column(
        db.Integer, db.ForeignKey('incoming_products.sku_id'), unique=True)
    color = db.Column(db.String)
    material = db.Column(db.String)
    sleeve_type = db.Column(db.String)
    size = db.Column(db.String)

    def __init__(self, incoming_product_id, incoming_product_sku_id, color, material, sleeve_type, size):
        self.incoming_product_id = incoming_product_id
        self.incoming_product_sku_id = incoming_product_sku_id
        self.color = color
        self.material = material
        self.sleeve_type = sleeve_type
        self.size = size

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'incoming_product_id': self.incoming_product_id,
            'incoming_product_sku_id': self.incoming_product_sku_id,
            'color': self.color,
            'material': self.material,
            'sleeve_type': self.sleeve_type,
            'size': self.size
        }


class ProductSupplier(db.Model):
    __tablename__ = 'product_supplier'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('incoming_products.id'))
    product_sku_id = db.Column(
        db.Integer, db.ForeignKey('incoming_products.sku_id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    def __init__(self, product_id, product_sku_id, supplier_id):
        self.product_id = product_id
        self.product_sku_id = product_sku_id
        self.supplier_id = supplier_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_sku_id': self.product_sku_id,
            'supplier_id': self.supplier_id
        }
