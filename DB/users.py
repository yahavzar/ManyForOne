import email
from server.utils import send_mail
from DB.db_init import *
from server.utils import get_coordinates

BAD_RATING = 0


class User(db.Model):
    # email is the primary_key
    email = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)  # a string of address
    status_text = db.Column(db.String, nullable=False)
    coordinates = db.Column(db.String, nullable=True)  # a list of coordinates like "[34.766968, 32.085620]"
    password = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    rating_counter = db.Column(db.Integer, nullable=False, default=0)
    tagging_score = db.Column(db.Integer, nullable=False, default=0)
    donation_counter = db.Column(db.Integer, nullable=False, default=0)
    delivery_counter = db.Column(db.Integer, nullable=False, default=0)
    picture = db.Column(db.String, nullable=True)
    donations = db.relationship('Donation', backref='owner_user', lazy=True)
    contribution_rank = db.Column(db.Integer, nullable=False)
    suspicious_days = db.Column(db.Integer, nullable=False, default=0)
    suspicious_requests_today = db.Column(db.Integer, nullable=False, default=0)


def add_new_user(email, name, location, password, tagging_score=1, donation_counter=0,
                 delivery_counter=0, picture=None, contribution_rank=0,
                 status_text="Roses are red, Violets are blue, If I'll have something tasty, I'll share it with you"):
    """
    :return: user object / EmailExistsInDB exception / general exception
    """
    try:
        coordinates = str(get_coordinates(address=location))
    except:
        coordinates = None

    new_user = User(email=email, name=name, location=location, coordinates=coordinates, password=password,
                    tagging_score=tagging_score, donation_counter=donation_counter, delivery_counter=delivery_counter,
                    picture=picture, contribution_rank=contribution_rank, status_text=status_text)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user

    except IntegrityError as e:
        db.session.rollback()
        # might be unique error - check if the email already exists
        user = get_user(email=email)
        if user:
            db_logger.info("add_new_user failed with error EmailExistsInDB")
            raise EmailExistsInDB(email)
        else:
            db_logger.error("func: add_new_user failed with error %s" % e)
            raise e

    except Exception as e:
        db_logger.error("func: add_new_user failed with error %s" % e)
        raise e


def get_suspicious_requests_today(email):
    user = User.query.filter_by(email=email).first()
    return user.suspicious_requests_today


def get_suspicious_days(email):
    user = User.query.filter_by(email=email).first()
    return user.suspicious_days


def update_suspicious_days(email):
    user = User.query.filter_by(email=email).first()
    user.suspicious_days += 1
    db.session.commit()


def delete_suspicious_days(email):
    user = User.query.filter_by(email=email).first()
    user.suspicious_days = 0
    db.session.commit()


def update_suspicious_requests_today(email):
    user = User.query.filter_by(email=email).first()
    user.suspicious_requests_today += 1
    db.session.commit()


def update_rating_counter(email):
    user = User.query.filter_by(email=email).first()
    user.rating_counter += 1
    db.session.commit()


def get_user(email):
    """
    :param email:
    :return: user object if exists in db, else None
    """
    user = User.query.filter_by(email=email).first()
    return user


def remove_user(email):
    user = get_user(email)
    if user:
        db.session.delete(user)
        db.session.commit()


def get_status_text(email):
    user = get_user(email)
    return user.status_text


def update_status_text(email, status_text):
    user = get_user(email)
    user.status_text = status_text
    db.session.commit()


def get_tagging_score(email):
    user = get_user(email)
    return user.tagging_score


def update_tagging_score(email):
    user = get_user(email)
    user.tagging_score += 1
    db.session.commit()


def update_user_details(email, password, location, status, img_path):
    user = get_user(email)
    user.password = password
    user.location = location
    user.coordinates = str(get_coordinates(location))
    user.status_text = status
    user.picture = img_path
    db.session.commit()


def reset_contribution_ranks():
    for user in User.query.all():
        user.contribution_rank = 0
    db.session.commit()


def update_contribution_rank(user_object, rank_int):
    user_object.contribution_rank = rank_int
    db.session.commit()


def get_users_list():
    return User.query.all()


def update_all_contribution_ranks():
    reset_contribution_ranks()
    for user in get_users_list():
        if user.rating is  None:
            rate = 0
        else:
            rate=user.rating
        rank_int = user.donation_counter * 2 + user.delivery_counter * 2 + user.tagging_score + rate
        update_contribution_rank(user, rank_int)
    email_top_contributors()


def email_top_contributors():
    users = get_top_5_users()
    for user in users:
        if user:
            send_mail(title="Congratulations! You Are A Top Contributor!",
                      body="We are happy to inform you that you are in the top 5 contributors to our website.\n"
                           "We would like to thank you for you help and efforts, they are greatly appreciated.\n"
                           "Your picture and status will be displayed in our home page for the next day.\n"
                           "Your current status is: \n%s\n"
                           "If you wish to edit your status you can do so using 'edit details' in your profile page.\n"
                           "Thank you and have a great day!\n'Many for One' Administration" % user.status_text,
                      recipients=[user.email])

def get_top_5_users():
    newlist = sorted(get_users_list(), key=lambda x: x.contribution_rank, reverse=True)
    top5 = newlist[0:5]
    while len(top5) < 5:
        top5.append(None)
    return top5


def get_user_with_contribution_rank(contribution_rank):
    """
    :param contribution_rank:
    :return: user object with the contribution_rank (assuming only one exists) or None if not found
    """
    user = User.query.filter_by(contribution_rank=contribution_rank).first()
    return user


def update_reliability(email, int_value, add=True):
    user = User.query.filter_by(email=email).first()
    if not user:
        return
    if user.rating == None:
        user.rating = 0
    if add:
        value = int_value
    else:
        value = 0 - int_value
    rating_counter = user.rating_counter
    user.rating = (user.rating * rating_counter + value) / (rating_counter + 1)
    user.rating_counter += 1
    db.session.commit()


def return_bad_users_ratings():
    users = User.query.all()
    bad_users = set()
    for user in users:
        if user.rating is not None and user.rating <= BAD_RATING:
            bad_users.add(user.email)
    return bad_users


