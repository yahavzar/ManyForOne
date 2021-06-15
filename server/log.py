import json
import threading
from flask import request, render_template, Blueprint, session, jsonify, redirect
from tornado.escape import json_encode
from DB.requests import *
from DB.donations import *
from DB.users import *

log_page = Blueprint('Log', __name__, template_folder='../templates')


@log_page.route('/log', methods=['POST', 'GET'])
def index():
    if 'email' not in session:
        return redirect("/Login")
    if request.method != 'POST':

        user_email = session['email']

        open_requests_by_user = get_all_requests_by_user(user_email=user_email,
                                                         request_status=RequestStatus.By_recipient)
        open_requests_by_user.extend(
            get_all_requests_by_user(user_email=user_email, request_status=RequestStatus.In_process))
        open_requests_by_user.extend(
            get_all_requests_by_user(user_email=user_email, request_status=RequestStatus.By_volunteer))

        open_requests_rows = []
        for request_obj in open_requests_by_user:
            request_id = request_obj.id
            donor_obj = get_user(request_obj.donor)
            name = donor_obj.name
            quantity = request_obj.recipients_amount
            status = RequestStatus(request_obj.status).name
            if status == RequestStatus.By_recipient.name:
                progress = '20'
            else:
                progress = '60'
            date = request_obj.date
            volunteer = ''
            if status == RequestStatus.In_process.name:
                volunteer = '1'
            elif status == RequestStatus.By_recipient.name:
                volunteer = '0'
            open_requests_rows.append(
                {"name": name, "id": request_id, 'progress': progress, 'quantity': quantity, 'volunteer': volunteer,
                 'date': str(date), 'rating_delivery': 'fill', 'rating_donor': 'fill'})

        done_requests_by_user = get_all_requests_by_user(user_email=user_email, request_status=RequestStatus.Delivered)
        done_requests_by_user.extend(
            get_all_requests_by_user(user_email=user_email, request_status=RequestStatus.Missing))

        done_requests_rows = []
        for request_obj in done_requests_by_user:
            request_id = request_obj.id
            donor_obj = get_user(request_obj.donor)
            name = donor_obj.name
            quantity = request_obj.recipients_amount
            status = RequestStatus(request_obj.status).name
            date = request_obj.date
            donor_rating = request_obj.donor_rating
            volunteer_rating = request_obj.volunteer_rating
            volunteer='0'
            if request_obj.volunteer != None:
                volunteer = '1'
            if status == RequestStatus.Delivered.name:
                progress = '100'
                is_complete = '1'

            else:
                progress = '60'
                is_complete = '0'

            done_requests_rows.append(
                {"name": name, "id": request_id, 'status': status, 'progress': progress, 'quantity': quantity,'volunteer' : volunteer,
                 'date': str(date), 'rating_delivery': volunteer_rating, 'rating_donor': donor_rating,
                 'complete': is_complete})

        return render_template("log.html", res=done_requests_rows, res2=open_requests_rows)

    if request.method == "POST":
        table_rows = json.loads(request.form.get('data'))
        for row in table_rows:
            if 'update' in row:
                request_obj = get_request(row['id'])
                if 'status' in row:
                    if row['status'] == 'confirmed':
                        update_request_Delivered(request_id=row['id'])
                        args = ("Status Update - The donation has been received",
                                "We would like to thank you for your help.",
                                [request_obj.donor],)
                        threading.Thread(target=send_mail, args=args).start()
                    else:
                        update_request_Missing(request_id=row['id'])
                        if row['volunteer'] == '1':
                            update_volunteer_rating(request_id=row['id'], add=False, diff_int=1)
                            update_reliability(request_obj.volunteer, int_value=1, add=False)
                            args = ("Status Update - The donation is missing",
                                    "If you have any information regarding the lost donation with request number %s "
                                    "please contact us in this mail: taumanyforone@gmail.com" % request_obj.id,
                                    [request_obj.volunteer],)
                            threading.Thread(target=send_mail, args=args).start()

                        else:
                            update_donor_rating(request_id=row['id'], add=False, diff_int=1)
                            update_reliability(request_obj.donor, int_value=1, add=False)
                            args = ("Status Update - The donation is missing",
                                    "If you have any information regarding the lost donation with request number %s "
                                    "please contact us in this mail: taumanyforone@gmail.com" % request_obj.id,
                                    [request_obj.donor],)
                            threading.Thread(target=send_mail, args=args).start()

                if 'rating_donor' in row and row['rating_donor'] != 'fill':
                    update_donor_rating(request_id=row['id'], diff_int=int(row['rating_donor']))
                    update_reliability(request_obj.donor, int_value=int(row['rating_donor']))
                if 'rating_delivery' in row and row['rating_delivery'] != 'fill' and request_obj.volunteer != None :
                    update_volunteer_rating(request_id=row['id'], diff_int=int(row['rating_delivery']))
                    update_reliability(request_obj.volunteer, int_value=int(row['rating_delivery']))

        return redirect('/log')


@log_page.route('/volunteer_log', methods=['POST', 'GET'])
def index2():
    if 'email' not in session:
        return redirect("/Login")
    if request.method != 'POST':

        user_email = session['email']

        open_requests_by_volunteer = get_all_requests_by_volunteer(user_email=user_email,
                                                                   request_status=RequestStatus.In_process)
        open_requests_by_volunteer.extend(
            get_all_requests_by_volunteer(user_email=user_email, request_status=RequestStatus.By_volunteer))

        open_requests_rows = []
        for request_obj in open_requests_by_volunteer:
            request_id = request_obj.id
            donor_obj = get_user(request_obj.donor)
            name = donor_obj.name
            quantity = request_obj.recipients_amount
            status = RequestStatus(request_obj.status).name
            if status == RequestStatus.By_recipient.name:
                progress = '20'
            else:
                progress = '60'
            date = request_obj.date
            volunteer = ''
            if status == RequestStatus.In_process.name:
                volunteer = '1'
            elif status == RequestStatus.By_recipient.name:
                volunteer = '0'
            location = get_user(request_obj.recipient).location
            open_requests_rows.append(
                {"name": name, "id": request_id, 'progress': progress, 'quantity': quantity, 'volunteer': volunteer,
                 'date': str(date), 'location': location})

        done_requests_by_volunteer = get_all_requests_by_volunteer(user_email=user_email,
                                                                   request_status=RequestStatus.Delivered)
        done_requests_by_volunteer.extend(
            get_all_requests_by_volunteer(user_email=user_email, request_status=RequestStatus.Missing))

        done_requests_rows = []
        for request_obj in done_requests_by_volunteer:
            request_id = request_obj.id
            donor_obj = get_user(request_obj.donor)
            name = donor_obj.name
            quantity = request_obj.recipients_amount
            status = RequestStatus(request_obj.status).name
            date = request_obj.date
            donor_rating = request_obj.donor_rating
            volunteer_rating = request_obj.volunteer_rating
            if status == RequestStatus.Delivered.name:
                progress = '100'
                is_complete = '1'
            else:
                progress = '60'
                is_complete = '0'

            done_requests_rows.append(
                {"name": name, "id": request_id, 'status': status, 'progress': progress, 'quantity': quantity,
                 'date': str(date),
                 'complete': is_complete})

        return render_template("log-volunteer.html", res=done_requests_rows, res2=open_requests_rows)


@log_page.route('/donor_log', methods=['POST', 'GET'])
def index3():
    if 'email' not in session:
        return redirect("/Login")
    user_email = session['email']

    open_requests_by_donor = get_all_requests_by_donor(user_email=user_email, request_status=RequestStatus.By_recipient)
    open_requests_by_donor.extend(
        get_all_requests_by_donor(user_email=user_email, request_status=RequestStatus.In_process))
    open_requests_by_donor.extend(
        get_all_requests_by_donor(user_email=user_email, request_status=RequestStatus.By_volunteer))

    open_requests_rows = []
    for request_obj in open_requests_by_donor:
        request_id = request_obj.id
        recipient_obj = get_user(request_obj.recipient)
        recipient_name = recipient_obj.name
        volunteer_obj = get_user(request_obj.volunteer)
        volunteer_name = ""
        if volunteer_obj != None:
            volunteer_name = volunteer_obj.name
        quantity = request_obj.recipients_amount
        status = RequestStatus(request_obj.status).name
        if status == RequestStatus.By_recipient.name:
            progress = '20'
        else:
            progress = '60'
        date = request_obj.date
        volunteer = ''
        if status == RequestStatus.In_process.name:
            volunteer = '1'
        elif status == RequestStatus.By_recipient.name:
            volunteer = '0'
        open_requests_rows.append(
            {"recipient_name": recipient_name, "volunteer_name": volunteer_name, "id": request_id, 'progress': progress,
             'quantity': quantity, 'volunteer': volunteer,
             'date': str(date)})

    done_requests_by_donor = get_all_requests_by_donor(user_email=user_email, request_status=RequestStatus.Delivered)
    done_requests_by_donor.extend(
        get_all_requests_by_donor(user_email=user_email, request_status=RequestStatus.Missing))

    done_requests_rows = []
    for request_obj in done_requests_by_donor:
        request_id = request_obj.id
        donor_obj = get_user(request_obj.donor)
        name = donor_obj.name
        quantity = request_obj.recipients_amount
        status = RequestStatus(request_obj.status).name
        date = request_obj.date

        if status == RequestStatus.Delivered.name:
            progress = '100'
            is_complete = '1'
        else:
            progress = '60'
            is_complete = '0'

        done_requests_rows.append(
            {"name": name, "id": request_id, 'status': status, 'progress': progress, 'quantity': quantity,
             'date': str(date),
             'complete': is_complete})

    return render_template("log-donor.html", res=done_requests_rows, res2=open_requests_rows)

    return redirect('/donor_log')
