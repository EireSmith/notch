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

def flash_message(message, category="info"):
    flash(message, category)

def safe_redirect(endpoint, **kwargs):
    if endpoint in ["views.index", "views.invoices"]:
        return redirect(url_for(endpoint, **kwargs))
    flash_message("Invalid redirect.", "error")
    return redirect(url_for("views.index"))

def user_has_permission(contract_id, user_id):
    user_contracts = Contract.query.with_entities(Contract.id).filter(Contract.user_id == user_id).all()
    user_contract_ids = [contract[0] for contract in user_contracts]

    print(f"Contract ID: {contract_id}, User Contract IDs: {user_contract_ids}")  # Debugging line
    if int(contract_id) in user_contract_ids:
        return True
    else:
        return False


@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    try:
        curr_user = current_user.id

        # get all contract data
        contract_query = Contract.query.filter(Contract.user_id == curr_user).all()

        # Prepare lists for graph and averages
        start_dates_list = [str(i.date_start) for i in contract_query]
        end_dates_list = [str(i.date_end) for i in contract_query]
        contract_name_list = [str(i.job_title) for i in contract_query]
        rates = [int(i.pay_rate) for i in contract_query if i.pay_rate is not None]

        # Prepare graph data and averages
        graph_data = graph_structure(start_dates_list, contract_name_list)
        int_average_days = average_days(start_dates_list, end_dates_list)
        int_average_pay = average_pay(rates)

        # Handle form submission
        if request.method == "POST":
            date_format = "%Y-%m-%d"
            job = request.form.get("job", "")
            start = request.form.get("start") or str(datetime.date.today())
            end = request.form.get("end") or str(datetime.date.today())
            pay = request.form.get("pay") or 0

            try:
                start_date = datetime.datetime.strptime(start, date_format)
                end_date = datetime.datetime.strptime(end, date_format)
                pay = int(pay)
            except (ValueError, TypeError):
                flash_message("Invalid input. Please check your data.", "error")
                return redirect(url_for("views.index"))

            new_contract = Contract(
                job_title=job,
                date_start=start_date,
                date_end=end_date,
                pay_rate=pay,
                user_id=curr_user,
            )
            try:
                db.session.add(new_contract)
                db.session.commit()
                flash_message("Notch added", "success")
            except Exception as e:
                db.session.rollback()
                flash_message("Database error: could not add contract.", "error")
            return redirect(url_for("views.index"))

        # Get invoiced contracts for button styling
        try:
            invoiced_contracts = Invoice.get_user_invoiced_contracts(curr_user)
        except Exception:
            invoiced_contracts = []

        first_name = current_user.first_name
        first_name_init = first_name[0] if first_name else ""
        family_name_init = current_user.family_name[0] if current_user.family_name else ""

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
    except Exception as e:
        flash_message("An unexpected error occurred.", "error")
        return redirect(url_for("views.index"))


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
    date_format = "%Y-%m-%d"
    try:
        # parse JSON data
        json_file = json.loads(request.data)
        contract_id = json_file.get("contract_id")
        job = json_file.get("job", "")
        start = json_file.get("start", "")
        end = json_file.get("end", "")
        pay = json_file.get("pay", "")

        contract = Contract.query.get_or_404(contract_id)
        if contract.user_id != current_user.id:
            flash_message("Permission denied.", "error")
            return jsonify({"error": "Permission denied"}), 403
        
        start_date = None
        end_date = None
        if start:
            try:
                start_date = datetime.datetime.strptime(start, date_format)
            except ValueError:
                flash_message("Invalid start date format.", "error")
                return jsonify({"error": "Invalid start date"}), 400
        if end:
            try:
                end_date = datetime.datetime.strptime(end, date_format)
            except ValueError:
                flash_message("Invalid end date format.", "error")
                return jsonify({"error": "Invalid end date"}), 400

# if both dates are provided, check order
        if start_date and end_date:
            if end_date < start_date:
                flash_message("End date must be after start date.", "error")
                return jsonify({"error": "End date must be after start date"}), 400
        # if end is provided, compare with existing start
        elif end_date and not start_date:
            if contract.date_start:
                # make sure both are datetime objects to compare sucessfully
                contract_start = contract.date_start
                if isinstance(contract_start, datetime.date) and not isinstance(contract_start, datetime.datetime):
                    contract_start = datetime.datetime.combine(contract_start, datetime.time.min)
                if end_date < contract_start:
                    flash_message("End date must be after start date.", "error")
                    return jsonify({"error": "End date must be after start date"}), 400
        # if start is provided, compare with existing end
        elif start_date and not end_date:
            if contract.date_end:
                contract_end = contract.date_end
                if isinstance(contract_end, datetime.date) and not isinstance(contract_end, datetime.datetime):
                    contract_end = datetime.datetime.combine(contract_end, datetime.time.min)
                if contract_end < start_date:
                    flash_message("End date must be after start date.", "error")
                    return jsonify({"error": "End date must be after start date"}), 400

        # update fields after validation
        if job:
            contract.job_title = job
        if start_date:
            contract.date_start = start_date
        if end_date:
            contract.date_end = end_date
            
        if pay != "":
            try:
                contract.pay_rate = int(pay)
            except ValueError:
                flash_message("Invalid pay rate.", "error")
                return jsonify({"error": "Invalid pay rate"}), 400

        try:
            db.session.commit()
            flash_message("Notch has been updated.", "success")
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
            flash_message("Database error: could not update contract.", "error")
            return jsonify({"error": "Database error"}), 500

    except Exception as e:
        flash_message("An unexpected error occurred.", "error")
        return jsonify({"error": "Unexpected error"}), 500

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
