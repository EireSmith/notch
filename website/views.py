
from io import BytesIO
from flask import render_template, request, flash, jsonify, Blueprint, send_file, redirect, url_for
from .models import Contract, Invoice
from flask_login import login_required, current_user
from . import db
import datetime
import json
from .averages import average_days, average_pay

views = Blueprint('views', __name__)
 

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
  #declare empty lists to hold dates to compare
  start_dates_list=[]
  end_dates_list=[]

  #get data from current user
  curr_user = current_user.id
  contract_query = Contract.query.filter(Contract.user_id == curr_user).all()
  
  #populate date lists with string values
  for s in contract_query:
    s = str(s.date_start)
    start_dates_list.append(s)

  for e in contract_query:
    e = str(e.date_end)
    end_dates_list.append(e)
  
  int_average_days = average_days(start_dates_list, end_dates_list)

  rates = []
  for r in contract_query:
    r = int(r.pay_rate)
    rates.append(r)

  int_average_pay = average_pay(rates)

  
  if request.method == 'POST':
        date_format = '%Y-%m-%d'
        job = request.form.get('job')
        start = request.form.get('start')
        end = request.form.get('end')
        pay = request.form.get('pay')

        if job == None:
          job = ""
        if start == "" or start == None:
          start = str(datetime.date.today())
        start= datetime.datetime.strptime(start, date_format) #parsing HTML data type of string to date object
        if end == "" or end == None:
          end =str(datetime.date.today())
        end= datetime.datetime.strptime(end, date_format)
        if pay == None or pay == "":
          pay = 0

        new_contract = Contract(job_title=job, date_start=start, date_end=end, pay_rate=pay, user_id=current_user.id)
        db.session.add(new_contract)
        db.session.commit()
        flash('notch added', category='success')
       
  first_name= current_user.first_name
  first_name_init =list(first_name)[0]
  family_name_init = list(current_user.family_name)[0]
  return render_template("index.html", user = current_user, first_name = first_name, first_name_init = first_name_init, family_name_init = family_name_init, average_days = int_average_days, average_pay = int_average_pay)




@views.route('/delete_notch', methods=["POST"])
@login_required
def delete_contract():
  json_file = json.loads(request.data) # take in data as post req
  contract_id= json_file["contract_id"]
  contract = Contract.query.get_or_404(contract_id)
  if contract:
    if contract.user_id == current_user.id:
      db.session.delete(contract)
      db.session.commit()
  return jsonify({}) #empty json dict




@views.route('/update_notch', methods=['POST'])
@login_required
def update_contract():
      date_format = '%Y-%m-%d'
      json_file = json.loads(request.data) # take in data as post req
      contract_id= json_file["contract_id"]
      contract = Contract.query.get_or_404(contract_id)
      job = json_file["job"]
      start = json_file["start"]
      end = json_file["end"]
      pay = json_file["pay"]
      
      if contract:
        if contract.user_id == current_user.id:
          if job == "":
            contract.job_title = contract.job_title
          else:
            contract.job_title = job
          
          if start == "":
            contract.date_start =  contract.date_start
            
          else:
            start = datetime.datetime.strptime(start,  date_format)
            contract.date_start = start
            
          if end == "":
            contract.date_end = contract.date_end
            
          else:
            end = datetime.datetime.strptime(end,  date_format)
            contract.date_end = end

          if pay == "":
            contract.pay_rate = contract.pay_rate
          else:
            contract.pay_rate = pay

          db.session.commit()
          flash('notch has been Updated', category="success")
          return jsonify({}) #empty json dict


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_invoice():
  if request.method == 'POST':
     # takes in contract_id  from URL
      contract_id = request.args.get('id')
      user_contracts = Contract.query.with_entities(Contract.id).filter(Contract.user_id == current_user.id).all()
      permission = False
      for u in user_contracts:
        if int(contract_id) in u:
          permission = True

      exists = Invoice.query.filter(Invoice.contract_id == contract_id).first() #checking if invoice exists
      if exists or permission == False:
        flash('invoice already attached', category="error")
      else:
        #  takes file from submit form
        file = request.files["file"]
        # adds invoice to database
        invoice = Invoice(filename=file.filename, invoice_data = file.read(), contract_id = contract_id)
        db.session.add(invoice)
        db.session.commit()
        return redirect(url_for("views.index"))
  return render_template("upload.html", user = current_user)



@views.route('/download/<int:id>', methods=['GET'])
@login_required
def download_invoice(id):
  
  user_contracts = Contract.query.with_entities(Contract.id).filter(Contract.user_id == current_user.id).all()
  for u in user_contracts:
    if id in u:
      invoice = Invoice.query.filter_by(contract_id = id).first()
      if invoice:
        return send_file(BytesIO(invoice.invoice_data), attachment_filename=invoice.filename, as_attachment=True)

  flash('no invoice attatched', category="error")
  return redirect(url_for("views.index"))

@views.route('/invoices', methods =["GET"])
@login_required
def search():

  first_name= current_user.first_name
  first_name_init =list(current_user.first_name)[0]
  family_name_init = list(current_user.family_name)[0]
  invoice_ids = Invoice.get_user_invoice(current_user.id)
  return render_template("invoices.html", invoices = invoice_ids, user = current_user, first_name = first_name, first_name_init = first_name_init, family_name_init = family_name_init)

#error pages
#invalid URL
@views.errorhandler(404)
def page_not_found(e):
  return render_template("error_pages/404.html"), 404

@views.errorhandler(500)
def page_not_found(e):
  return render_template("error_pages/500.html"), 500

