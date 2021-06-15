from DB.db_init import *
from DB import del_all_user_donations, del_all_donations
from DB.requests import get_all_requests_per_day, calc_avg_requests_per_day, del_all_requests
from DB.users import get_suspicious_requests_today, update_suspicious_days, get_suspicious_days, delete_suspicious_days, \
    return_bad_users_ratings, get_user
import threading
from server.utils import send_mail

SUSPICIOUS_AMOUNT_OF_DAYS = 3
GOOD_RATING = 5

class Suspicious(db.Model):
    # email is the primary_key
    email = db.Column(db.String, primary_key=True, nullable=False)


def add_to_Suspicious(email):
    new_row = Suspicious(email=email)
    if not is_in_Suspicious(email):
        db.session.add(new_row)
        db.session.commit()


def remove_from_suspicious_list(email):
    user = Suspicious.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()


def is_in_Suspicious(email):
    """
    :param email:
    :return: True is in Blacklist, False otherwise
    """
    user = Suspicious.query.filter_by(email=email).first()
    if not user:
        return False
    return True


def get_all_suspicious_users():
    all_suspicious_users = Suspicious.query.all()
    return [s.email for s in all_suspicious_users]


def check_suspicious_users():
    # Inserting new people to suspicious list
    check_suspicious_days()
    users = return_bad_users_ratings()
    suspicious_users = get_all_suspicious_users()
    for user in users:
        if user not in get_all_suspicious_users():
            args = ("Important notice!",
                    "You've been reported by several users.\n"
                    "Your account may be deleted soon. If you think this is a mistake\n"
                    "please contact us using via mail: taumanyforone@gmail.com",
                    [user],)
            threading.Thread(target=send_mail, args=args).start()
            add_to_Suspicious(user)
    # Remove users with high rating
    suspicious_users_emails = get_all_suspicious_users()
    for user_email in suspicious_users_emails:
        user = get_user(user_email)
        if user.rating >= GOOD_RATING:
            remove_from_suspicious_list(user_email)


def check_suspicious_days():
    requests = get_all_requests_per_day()
    users_list = set()
    for request in requests:
        users_list.add(request.recipient)

    avg_requests = calc_avg_requests_per_day()
    for user in users_list:
        # The amount of suspicious requests per day is greater than the average amount of requests for that day
        if (get_suspicious_requests_today(user) > avg_requests) or ((len(users_list) == 1) and (get_suspicious_requests_today(user) >= 5)):
            update_suspicious_days(user)
        # Check if the user behaved suspiciously 3 days. If yes, insert to suspicious list
        if get_suspicious_days(user) >= SUSPICIOUS_AMOUNT_OF_DAYS and user not in get_all_suspicious_users():
            args = ("Important notice!",
                    "We detected suspicious behavior in your account.\n"
                    "Your account may be deleted soon. If you think this is a mistake\n"
                    "please contact us using via mail: taumanyforone@gmail.com",
                    [user],)
            threading.Thread(target=send_mail, args=args).start()
            add_to_Suspicious(user)
