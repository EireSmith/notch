
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


  # return invoices for current user
  def get_user_invoice(id):
        invoices = db.session.query(Contract.job_title, Contract.id, Invoice.filename).select_from(Invoice).join(Contract).join(User).filter(User.id == id).all()
        
        return invoices
  
  # Get List of Contract IDs which contain an Invoice
  def get_user_invoiced_contracts(id):
      invoice_contract_ids = db.session.query(Invoice.contract_id).join(Contract).filter(Contract.user_id == id).all()
      invoice_contract_ids = [item for i in invoice_contract_ids for item in i]

      return invoice_contract_ids
