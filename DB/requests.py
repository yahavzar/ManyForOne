import threading

from sqlalchemy import extract
from DB.db_init import *
from DB.frequency import update_frequency
from DB.users import User
from DB.donations import Donation, get_donation
from enum import Enum
from datetime import datetime

from server.utils import send_mail


class RequestStatus(Enum):
    By_volunteer = 0
    By_recipient = 1
    In_process = 2
    Delivered = 3
    Missing = 4


class Request(db.Model):
    # id is the primary_key
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    recipient = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    donor = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    volunteer = db.Column(db.String, db.ForeignKey('user.email'), nullable=True)
    donation = db.Column(db.Integer, db.ForeignKey('donation.id'), nullable=False)
    recipients_amount = db.Column(db.Integer, nullable=False)  # <= donation.recipients_amount
    status = db.Column(db.Integer, nullable=False)  # RequestStatus
    donor_rating = db.Column(db.Integer, nullable=True, default=0)
    volunteer_rating = db.Column(db.Integer, nullable=True, default=0)


def del_all_requests():
    requests = Request.query.all()
    for request in requests:
        db.session.delete(request)
        db.session.commit()


def delete_user_requests(email):
    requests = Request.query.filter_by(recipient=email).all()
    for request in requests:
        db.session.delete(request)
        db.session.commit()


def calc_avg_requests_per_day():
    requests = get_all_requests_per_day()
    users_list = set()
    for request in requests:
        users_list.add(request.recipient)

    avg_requests = 0
    if len(users_list) != 0:
        avg_requests = len(requests) / len(users_list)
    return avg_requests


# Returns all the donations that were requested in a certain day
def get_all_requests_per_day():
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year
    request_date = datetime(current_year, current_month, current_day)
    requests = Request.query.filter(extract('month', Request.date) >= request_date.month,
                                    extract('year', Request.date) >= request_date.year,
                                    extract('day', Request.date) >= request_date.day).all()
    return requests


def add_new_request(recipient, donation, recipients_amount, status=RequestStatus.By_recipient.value, volunteer=None,
                    donor=None):
    """
    :param recipient: id (email) of the user that requested
    :param donor: id (email) of the user that opened the donation
    :param donation: id of the donation
    :param recipients_amount: how many the recipient asked for, <= donation.recipients_amount
    :param status: RequestStatus
    :param volunteer: id (email) of the user that will transfer the donation
    :return: obj of the new request / general exception
    """
    donation_obj = Donation.query.filter_by(id=donation).first()
    if not donor:
        donor = donation_obj.user
    left = donation_obj.recipients_amount - donation_obj.taken_quantity
    if recipients_amount > left:
        db_logger.warning(
            "func: add_new_request recipients_amount %s > donation.recipients_amount %s, updated recipients_amount to donation.recipients_amount" % (
                recipients_amount, left))
        recipients_amount = left
    new_request = Request(recipient=recipient, donor=donor, volunteer=volunteer, donation=donation,
                          recipients_amount=recipients_amount, status=status, date=datetime.utcnow())

    donation_obj.taken_quantity += recipients_amount
    if (donation_obj.recipients_amount - donation_obj.taken_quantity) == 0:
        donation_obj.is_open = False

    if status == RequestStatus.By_volunteer.value:
        # update requests counter in the donation
        donation_obj.open_requests_counter += 1

    # update frequency table
    update_frequency(recipient_email=recipient, donor_email=donor)

    try:
        db.session.add(new_request)
        db.session.commit()
        return new_request

    except Exception as e:
        db_logger.error("func: add_new_request failed with error %s" % e)
        raise e


def get_request(id):
    request = Request.query.filter_by(id=id).first()
    return request


def volunteer_taking_a_request(volunteer_id, request_id):
    """
    :param volunteer_id: id (email) of the user that will transfer the request
    :param request_id: id of the request to update
    :return: return True for success, False otherwise
    """
    is_success_volunteer = update_volunteer(volunteer_id, request_id)
    is_success_status = update_request_in_process(request_id)

    return is_success_volunteer and is_success_status


def update_volunteer(volunteer_id, request_id):
    """
    :param volunteer_id: id (email) of the user that will transfer the request
    :param request_id: id of the request to update
    :return: updates the volunteer's counter and sends a mail, return True for success, False otherwise
    """
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.volunteer = volunteer_id
        volunteer = User.query.filter_by(email=volunteer_id).first()
        volunteer.delivery_counter += 1
        donor_obj = User.query.filter_by(email=request.donor).first()
        recipient_obj = User.query.filter_by(email=request.recipient).first()

        args = ("Request %s"%request.id,
                "Thank you for volunteering to deliver the donation!\n"
                "Donor: %s\nRecipient: %s" % (donor_obj.location,recipient_obj.location),
                [volunteer_id],)
        threading.Thread(target=send_mail, args=args).start()

        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_volunteer failed with error %s" % e)
        return False


def update_request_in_process(request_id):
    """
    :param request_id: id of the request to update
    :return: return True for success, False otherwise
    """
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.status = RequestStatus.In_process.value

        donation_obj = Donation.query.filter_by(id=request.donation).first()

        # update requests counter in the donation
        donation_obj.open_requests_counter -= 1

        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_request_in_process failed with error %s" % e)
        return False


def update_request_Delivered(request_id):
    """
    :param request_id: id of the request to update
    :return: return True for success, False otherwise
    """
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.status = RequestStatus.Delivered.value
        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_request_Delivered failed with error %s" % e)
        return False


def update_request_Missing(request_id):
    """
    :param request_id: id of the request to update
    :return: return True for success, False otherwise
    """
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.status = RequestStatus.Missing.value
        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_request_Delivered failed with error %s" % e)
        return False


def update_donor_rating(request_id, diff_int, add=True):
    try:
        request = Request.query.filter_by(id=request_id).first()
        if add:
            request.donor_rating = request.donor_rating + diff_int
        else:
            request.donor_rating = request.donor_rating - diff_int
        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_donor_rating failed with error %s" % e)
        return False


def update_volunteer_rating(request_id, diff_int, add=True):
    try:
        request = Request.query.filter_by(id=request_id).first()
        if add:
            request.volunteer_rating = request.volunteer_rating + diff_int
        else:
            request.volunteer_rating = request.volunteer_rating - diff_int
        db.session.commit()
        return True

    except Exception as e:
        db_logger.error("func: update_volunteer_rating failed with error %s" % e)
        return False


def user_taking_donation(user_email, donation_id, amount):
    """
    :param user_email:
    :param donation_id:
    :param amount: how many from the total quantity
    :return:  obj of the new request / general exception
    """
    # add a successful request
    return add_new_request(recipient=user_email, donation=donation_id, recipients_amount=amount,
                           status=RequestStatus.By_recipient.value)


def get_all_requests_by_user(user_email, request_status=None):
    if request_status:
        all_requests = Request.query.filter_by(recipient=user_email, status=request_status.value).all()
    else:
        all_requests = Request.query.filter_by(recipient=user_email).all()
    return all_requests


def get_all_requests_by_donor(user_email, request_status=None):
    if request_status:
        all_requests = Request.query.filter_by(donor=user_email, status=request_status.value).all()
    else:
        all_requests = Request.query.filter_by(donor=user_email).all()
    return all_requests


def get_all_requests_by_volunteer(user_email, request_status=None):
    if request_status:
        all_requests = Request.query.filter_by(volunteer=user_email, status=request_status.value).all()
    else:
        all_requests = Request.query.filter_by(volunteer=user_email).all()
    return all_requests


def get_all_volunteer_requests_of_donation(donation_id):
    all_requests = Request.query.filter_by(donation=donation_id, status=RequestStatus.By_volunteer.value).all()
    return all_requests


def get_status_of_user(user_email):
    donor = 0
    volunteer = 0
    recipient = 0
    if (len(Request.query.filter_by(donor=user_email).all()) > 0):
        donor = 1
    if (len(Request.query.filter_by(volunteer=user_email).all()) > 0):
        volunteer = 1
    if (len(Request.query.filter_by(recipient=user_email).all()) > 0):
        recipient = 1
    return donor, volunteer, recipient
