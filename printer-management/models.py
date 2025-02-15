from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Printer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # available, assigned, maintenance
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assignments = db.relationship('Assignment', backref='printer', lazy=True)
    issues = db.relationship('Issue', backref='printer', lazy=True)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    assignments = db.relationship('Assignment', backref='seller', lazy=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    printer_id = db.Column(db.Integer, db.ForeignKey('printer.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, returned
    client = db.relationship('Client', backref='assignments')

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    printer_id = db.Column(db.Integer, db.ForeignKey('printer.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reported_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='open')  # open, resolved
