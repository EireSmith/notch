
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
from datetime import datetime

#Model Classes
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  family_name = db.Column(db.String(150))
  date_added = db.Column(db.DateTime(timezone=True), default=func.now())
  contracts = db.relationship('Contract')

class Contract(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  job_title = db.Column(db.String(150), nullable=False)
  date_start = db.Column(db.Date, nullable=False) 
  date_end = db.Column(db.Date)
  pay_rate = db.Column(db.Numeric(6,2))
  date_added = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
