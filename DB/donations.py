import json
from datetime import datetime, timedelta

from flask import session
from sqlalchemy.ext.mutable import MutableDict
from DB import *
from DB.db_init import *
from DB.tagging import *
from DB.users import User, update_tagging_score
from sqlalchemy.sql.expression import func

from Recommendations.collaborative_filtering import get_user_recommendations


class Donation(db.Model):
    # id is the primary_key
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    recipients_amount = db.Column(db.Integer, nullable=False)
    taken_quantity = db.Column(db.Integer, nullable=False, default=0)
    is_predictable = db.Column(db.Boolean, nullable=False)  # no recipients_amount specified => True
    description = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=True)
    start_time = db.Column(db.DateTime,
                           nullable=False)  # a Python datetime object, returned by time.strptime for example
    end_time = db.Column(db.DateTime, nullable=False)  # a Python datetime object, returned by time.strptime for example
    is_open = db.Column(db.Boolean, nullable=False)
    is_in_process = db.Column(db.Boolean, nullable=False)
    is_kosher = db.Column(db.Boolean, nullable=False)
    is_vegan = db.Column(db.Boolean, nullable=False)
    is_meat = db.Column(db.Boolean, nullable=False)
    is_dairy = db.Column(db.Boolean, nullable=False)
    is_gluten_free = db.Column(db.Boolean, nullable=False)
    suggested_tags = db.Column(MutableDict.as_mutable(db.JSON), nullable=True, default=dict)
    quantity_predictions = db.Column(MutableDict.as_mutable(db.JSON), nullable=True, default=dict)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('donations', lazy=False))
    open_requests_counter = db.Column(db.Integer, nullable=False, default=0)


def get_quantity_predictions_dict(donation_id):
    donation_obj = Donation.query.filter_by(id=donation_id).first()
    quantity_predictions_dict = json.loads(json.dumps(dict(donation_obj.quantity_predictions)))
    return quantity_predictions_dict


def save_quantity_predictions_dict(donation_id, quantity_predictions_dict):
    donation_obj = Donation.query.filter_by(id=donation_id).first()
    donation_obj.quantity_predictions = quantity_predictions_dict
    db.session.commit()


def add_new_donation(user_email, recipients_amount=None, is_predictable=False, description='', picture=None,
                     start_time=None, end_time=None, is_open=True, is_in_process=False, is_kosher=False, is_vegan=False,
                     is_meat=False, is_dairy=False, is_gluten_free=False, quantity_predictions=None):
    """
    :return: donation id / general exception
    """
    if not recipients_amount:
        recipients_amount = 1
        is_predictable = True
        quantity_predictions = {'Users': [], 'Predictions': []}

    if not start_time:
        start_time = datetime.utcnow()
    if not end_time:
        end_time = start_time + timedelta(hours=2)

    new_donation = Donation(user=user_email, recipients_amount=recipients_amount, is_predictable=is_predictable,
                            quantity_predictions=quantity_predictions,
                            description=description, picture=picture,
                            start_time=start_time, end_time=end_time, is_open=is_open, is_in_process=is_in_process,
                            is_kosher=is_kosher, is_vegan=is_vegan,
                            is_meat=is_meat, is_dairy=is_dairy, is_gluten_free=is_gluten_free)

    try:
        # update donation counter of user
        user = User.query.filter_by(email=user_email).first()
        user.donation_counter += 1
        db.session.add(new_donation)
        db.session.commit()
        return new_donation

    except Exception as e:
        db_logger.error("func: add_new_donation failed with error %s" % e)
        raise e


def get_donation(donation_id):
    donation = Donation.query.filter_by(id=donation_id).first()
    return donation


def get_donor(donation_id):
    donation = Donation.query.filter_by(id=donation_id).first()
    donor = User.query.filter_by(email=donation.user).first()
    return donor


def get_donation_labels(id):
    labels = []
    donation = Donation.query.filter_by(id=id).first()
    if donation.is_kosher:
        labels.append("Kosher")
    if donation.is_vegan:
        labels.append("Vegan")
    if donation.is_meat:
        labels.append("Meat")
    if donation.is_dairy:
        labels.append("Dairy")
    if donation.is_gluten_free:
        labels.append("Gluten Free")
    return ", ".join(labels)


def get_donation_image(id):
    donation = Donation.query.filter_by(id=id).first()
    return donation.picture


def get_user_donations(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user:
        return user.donations
    return None


def del_all_user_donations(user_email):
    donations = Donation.query.filter_by(user=user_email)
    for donation in donations:
        db.session.delete(donation)
        db.session.commit()


def del_all_donations():
    donations = Donation.query.all()
    for donation in donations:
        db.session.delete(donation)
        db.session.commit()


def get_all_donations():
    donations = Donation.query.all()
    return [donation.id for donation in donations]


def add_tag_to_donation(donation_obj, tag_obj):
    donation_obj.tags.append(tag_obj)
    db.session.commit()


def filter_donations_by_tags(tags_list):
    donations = db.session.query(Donation)
    for tag in tags_list:
        donations = donations.filter(Donation.tags.any(Tag.name == tag.name))
    return donations.all()


def filter_donations_by_tags_search(tags_list):
    donations = db.session.query(Donation)
    for tag in tags_list:
        donations = donations.filter(Donation.tags.any(Tag.name == tag))
    return donations.all()


def create_geojson(filter_dict=None, requests_list=None):
    if not filter_dict:
        open_donations = Donation.query.filter_by(is_open=True).all()
        geojson = geojson_from_donations_list(open_donations)
        return geojson

    # Volunteer view
    if filter_dict['volunteer_view'] == '1':
        open_donations = Donation.query.filter(Donation.open_requests_counter > 0)
        open_donations = open_donations.all()
        geojson = geojson_from_donations_list(open_donations, "Donations_Requests")
        return geojson

    # Recipient View
    open_donations = Donation.query.filter_by(is_open=True)

    # default tags
    if filter_dict["kosher"] == '1':
        open_donations = open_donations.filter_by(is_kosher=True)
    if filter_dict["Meat"] == '1':
        open_donations = open_donations.filter_by(is_meat=True)
    if filter_dict["Dairy"] == '1':
        open_donations = open_donations.filter_by(is_dairy=True)
    if filter_dict["Vegan"] == '1':
        open_donations = open_donations.filter_by(is_vegan=True)
    if filter_dict["gluten"] == '1':
        open_donations = open_donations.filter_by(is_gluten_free=True)

    # Tags Search:
    if len(filter_dict.getlist('tags_search')) != 0:
        tags_list = filter_dict.getlist('tags_search')
        for tag in tags_list:
            open_donations = open_donations.filter(Donation.tags.any(Tag.name == tag))

    open_donations = open_donations.all()

    # Recommendations view
    if filter_dict['recommendations_view'] == '1' and 'email' in session:
        recommended_donors = get_user_recommendations(user_email=session['email'], requests_list=requests_list)
        filtered_open_donations = []
        for donation_obj in open_donations:
            if donation_obj.user in recommended_donors:
                filtered_open_donations.append(donation_obj)
        open_donations = filtered_open_donations

    # Tagger View
    if filter_dict['tagger_view'] == '1':
        lowest_tags_count = get_lowest_tags_count()
        filtered_open_donations = []
        for donation_obj in open_donations:
            if len(donation_obj.tags) == lowest_tags_count:
                filtered_open_donations.append(donation_obj)
        open_donations = filtered_open_donations

    geojson = geojson_from_donations_list(open_donations)
    return geojson


def geojson_from_donations_list(donation_obj_list, uri="Donations"):
    geojson = {"type": "geojson", "data": {
        "type": "FeatureCollection",
        "features": []}}
    for donation in donation_obj_list:
        donor = get_donor(donation.id)
        if donor.coordinates is not None:
            donation_dict = {
                "type": "Feature",
                "properties": {
                    "description":
                        '<iframe '
                        f'src="/{uri}/{donation.id}" '
                        'style="border:2px solid black;" '
                        'height="430" width="700" '
                        'title="Iframe Example">'
                        '</ iframe>',
                    "icon": "theatre-15"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": eval(donor.coordinates)
                }
            }
            geojson["data"]["features"].append(donation_dict)
    geojson = str(geojson).replace("\'", "\"")
    return geojson


def get_lowest_tags_count():
    min_count = len(Tag.query.all())
    for donation_obj in Donation.query.all():
        if len(donation_obj.tags) < min_count:
            min_count = len(donation_obj.tags)
    return min_count
