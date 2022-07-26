
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

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
  invoice = db.relationship("Invoice", cascade="all,delete", back_populates="contract", uselist=False)
  
class Invoice(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String(255))
  invoice_data = db.Column(db.LargeBinary)
  date_added = db.Column(db.DateTime(timezone=True), default=func.now())
  contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
  contract = db.relationship("Contract", back_populates="invoice")

  def get_user_invoice(id):
      # return invoices for current user
        invoices = db.session.query(User.first_name, Contract.job_title, Invoice.id, Invoice.filename).select_from(Invoice).join(Contract).join(User).filter(User.id == id).all()
        return invoices
        
