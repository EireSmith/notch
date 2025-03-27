from io import BytesIO
from flask import (
    render_template,
    request,
    flash,
    jsonify,
    Blueprint,
    send_file,
    redirect,
    url_for,
)
from .models import Contract, Invoice, User
from flask_login import login_required, current_user
from . import db
import datetime
import json
from .file_type import allowed_file, allowed_filesize
from .averages import average_days, average_pay
from .chart import graph_structure
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def index():

    # get data from current user
    curr_user = current_user.id

    contract_query = Contract.query.filter(Contract.user_id == curr_user).all()

    start_dates_list = []
    end_dates_list = []
    contract_name_list = []
    rates = []

    # populate lists from query
    for i in contract_query:
        start_dates_list.append(str(i.date_start))
        end_dates_list.append(str(i.date_end))
        contract_name_list.append(str(i.job_title))
        rates.append(int(i.pay_rate))

    # call function to populate graph list
    graph_data = graph_structure(start_dates_list, contract_name_list)

    # get averages
    int_average_days = average_days(start_dates_list, end_dates_list)
    int_average_pay = average_pay(rates)

    # VALIDATING FORM DATA FOR DB SUBMISSION
    if request.method == "POST":
        date_format = "%Y-%m-%d"
        job = request.form.get("job")
        start = request.form.get("start")
        end = request.form.get("end")
        pay = request.form.get("pay")

        if job == None:
            job = ""
        if start == "" or start == None:
            start = str(datetime.date.today())
        start = datetime.datetime.strptime(
            start, date_format
        )  # parsing HTML data type of string to date object
        if end == "" or end == None:
            end = str(datetime.date.today())
        end = datetime.datetime.strptime(end, date_format)
        if pay == None or pay == "":
            pay = 0

        # SUBMITTING FORM DATA TO DB
        new_contract = Contract(
            job_title=job,
            date_start=start,
            date_end=end,
            pay_rate=pay,
            user_id=current_user.id,
        )
        db.session.add(new_contract)
        db.session.commit()
        flash("notch added", category="success")
        return redirect(url_for("views.index"))

    # GET INVOICED CONTRACTS TO CHANGE DOWNLAOD BUTTON STYLE
    invoiced_contracts = Invoice.get_user_invoiced_contracts(curr_user)
    first_name = current_user.first_name
    first_name_init = list(first_name)[0]
    family_name_init = list(current_user.family_name)[0]
    return render_template(
        "index.html",
        graph_data=graph_data,
        invoiced_contracts=invoiced_contracts,
        contract_query=contract_query,
        user=current_user,
        first_name=first_name,
        first_name_init=first_name_init,
        family_name_init=family_name_init,
        average_days=int_average_days,
        average_pay=int_average_pay,
    )


@views.route("/delete_notch", methods=["POST"])
@login_required
def delete_contract():
    json_file = json.loads(request.data)  # take in data as post req
    contract_id = json_file["contract_id"]
    contract = Contract.query.get_or_404(contract_id)
    if contract:
        if contract.user_id == current_user.id:
            db.session.delete(contract)
            db.session.commit()
    return jsonify({})  # empty json dict


@views.route("/update_notch", methods=["POST"])
@login_required
def update_contract():
    # ADD DATE FORMAT VARIABLE FOR DATETIME OBJECTS
    date_format = "%Y-%m-%d"

    # GET FORM DATA
    json_file = json.loads(request.data)  # take in data as post req
    contract_id = json_file["contract_id"]
    contract = Contract.query.get_or_404(contract_id)
    job = json_file["job"]
    start = json_file["start"]
    end = json_file["end"]
    pay = json_file["pay"]

    # VALIDATING UPDATE DATA
    if contract:
        if contract.user_id == current_user.id:
            if job == "":
                contract.job_title = contract.job_title
            else:
                contract.job_title = job

            if start == "":
                contract.date_start = contract.date_start

            else:
                start = datetime.datetime.strptime(start, date_format)
                contract.date_start = start

            if end == "":
                contract.date_end = contract.date_end

            else:
                end = datetime.datetime.strptime(end, date_format)
                contract.date_end = end

            if pay == "":
                contract.pay_rate = contract.pay_rate
            else:
                contract.pay_rate = pay

            db.session.commit()
            flash("notch has been Updated", category="success")
            return jsonify({})  # empty json dict


@views.route("/upload", methods=["GET", "POST"])
@login_required
def upload_invoice():
    if request.method == "POST":

        if not allowed_filesize(request.cookies.get("filesize")):
            flash("file must be less than 1mb", category="error")
            return redirect(url_for("views.index"))

        # takes file from submit form
        file = request.files["file"]
        # takes in contract_id  from URL
        contract_id = request.args.get("id")
        user_contracts = (
            Contract.query.with_entities(Contract.id)
            .filter(Contract.user_id == current_user.id)
            .all()
        )

        permission = False
        for u in user_contracts:
            if int(contract_id) in u:
                permission = True

        if permission == False:
            flash("access denied", category="error")
            return redirect(url_for("views.index"))

        exists = Invoice.query.filter(
            Invoice.contract_id == contract_id
        ).first()  # checking if invoice exists
        if exists:
            flash("invoice already attached", category="error")
            return redirect(url_for("views.index"))

        if not allowed_file(file.filename):
            flash("image extension not allowed", category="error")
            return redirect(url_for("views.index"))

        else:
            filename = secure_filename(file.filename)
            # adds invoice to database
            invoice = Invoice(
                filename=filename, invoice_data=file.read(), contract_id=contract_id
            )
            db.session.add(invoice)
            db.session.commit()
            flash("file upload successful", category="success")

            return redirect(url_for("views.index"))
    return render_template("upload.html", user=current_user)


@views.route("/download/<int:id>", methods=["GET"])
@login_required
def download_invoice(id):
    user_contracts = (
        Contract.query.with_entities(Contract.id)
        .filter(Contract.user_id == current_user.id)
        .all()
    )
    for u in user_contracts:
        if id in u:
            invoice = Invoice.query.filter_by(contract_id=id).first()
            if invoice:
                return send_file(
                    BytesIO(invoice.invoice_data),
                    attachment_filename=invoice.filename,
                    as_attachment=True,
                )

    flash("no invoice attatched", category="error")
    return redirect(url_for("views.index"))


@views.route("/invoices", methods=["GET"])
@login_required
def invoices():

    first_name = current_user.first_name
    first_name_init = list(current_user.first_name)[0]
    family_name_init = list(current_user.family_name)[0]
    # call function from models.py to get user invoices
    invoice_data = Invoice.get_user_invoice(current_user.id)
    return render_template(
        "invoices.html",
        invoices=invoice_data,
        user=current_user,
        first_name=first_name,
        first_name_init=first_name_init,
        family_name_init=family_name_init,
    )

@views.route("/user-profile", methods=["GET"])
@login_required
def user_profile():
    #info to populate HTML
    user_id = current_user.id
    first_name = current_user.first_name.capitalize()
    family_name = current_user.family_name.capitalize()


    return render_template("user-profile.html", user=current_user, user_id=user_id,first_name=first_name, family_name=family_name)

@views.route("/update_user", methods=["POST"])
@login_required
def update_user():

    json_file = json.loads(request.data)  # take in data as post req
    user_id = json_file["user_id"]
    user = User.query.get_or_404(user_id)
    first_name = json_file["first_name"]
    family_name = json_file["family_name"]

    if user:
        if user.id == current_user.id:
            if first_name == "":
                user.first_name = user.first_name
            else:
                user.first_name = first_name

            if family_name == "":
                user.family_name = user.family_name

            else:
                user.family_name = family_name

            db.session.commit()
            flash("user has been updated", category="success")
            return jsonify({}) 
    
    
    return jsonify({}) 
