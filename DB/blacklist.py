from DB.db_init import *
from DB.users import remove_user, User
from DB.requests import delete_user_requests
from DB.donations import del_all_user_donations


class Blacklist(db.Model):
    # email is the primary_key
    email = db.Column(db.String, primary_key=True, nullable=False)


def add_to_blacklist(email):
    blacklist_user = Blacklist(email=email)
    db.session.add(blacklist_user)
    # Remove user from the database, its donations and requests (everything related to the user)
    remove_user_data(email)
    db.session.commit()


def remove_user_data(email):
    user = User.query.filter_by(email=email)
    if user:
        user = user.first()
        if user:
            db.session.delete(user)
            db.session.commit()

    del_all_user_donations(email)
    delete_user_requests(email)


def is_in_blacklist(email):
    """
    :param email:
    :return: True is in Blacklist, False otherwise
    """
    user = Blacklist.query.filter_by(email=email).first()
    if not user:
        return False
    return True


def get_all_blacklisted_users():
    all_blacklisted_users = Blacklist.query.all()
    return [s.email for s in all_blacklisted_users]


def remove_from_blacklist(email):
    user = Blacklist.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
