from flask import Flask
from flask_testing import TestCase

from DB.users import *
from DB.donations import *
from DB.tagging import *
from DB.requests import *
from DB.frequency import *
import unittest

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    return app

class MyTest(TestCase):

    def create_app(self):
        return create_test_app()

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class UserseTest(MyTest):

    def test_add_user(self):
        add_new_user(email="test_mail", name="test_name", location="test_location", password="test_password")
        add_new_user(email="test_mail2", name="test_name2", location="test_location2", password="test_password")
        user = get_user(email="test_mail")
        user2 = get_user(email="test_mail2")
        assert user in db.session
        assert user.name == "test_name"
        assert user2.name == "test_name2"
        assert user.donation_counter == 0

    def test_email_exists(self):
        try:
            add_new_user(email="same_mail", name="test_name1", location="test_location", password="test_password")
            add_new_user(email="same_mail", name="test_name2", location="test_location", password="test_password")
        except Exception as e:
            assert type(e) == EmailExistsInDB
            assert e.message == "same_mail"

class DonationsTest(MyTest):
    def test_add_donation(self):
        user = add_new_user(email="donor_mail", name="test_name2", location="test_location2", password="test_password")
        donation_obj = add_new_donation(user_email="donor_mail", description='test', is_gluten_free=True)
        donation = get_donation(donation_obj.id)
        assert donation.user == user.email
        assert donation.is_gluten_free == True
        assert user.donation_counter == 1
        assert user.donations[0].id == 1

    def test_add_tags(self):
        tag1 = get_or_add_tag("tag1")
        tag2 = get_or_add_tag("tag2")
        user = add_new_user("donor1","","","")
        donation = add_new_donation("donor1",description="1")
        donation2 = add_new_donation("donor1",description="2")
        add_tag_to_donation(donation,tag1)
        add_tag_to_donation(donation,tag2)
        add_tag_to_donation(donation2, tag2)
        assert donation.tags[0].name == "tag1"
        assert donation.tags[1].name == "tag2"
        assert donation2.tags[0].name == "tag2"
        assert tag1.donations[0].description == "1"
        assert tag2.donations[0].description == "1"
        assert tag2.donations[1].description == "2"

    def test_filter_donations_by_tags(self):
        tag1 = get_or_add_tag("tag1")
        tag2 = get_or_add_tag("tag2")
        tag3 = get_or_add_tag("tag3")
        user = add_new_user("donor2","","","")
        donation1 = add_new_donation("donor2",description="1")
        donation2 = add_new_donation("donor2",description="2")
        add_tag_to_donation(donation1,tag1)
        add_tag_to_donation(donation1,tag2)
        add_tag_to_donation(donation2, tag2)
        add_tag_to_donation(donation2, tag3)
        donations_1_2 = filter_donations_by_tags([tag1,tag2])
        donations_2_3 = filter_donations_by_tags([tag2, tag3])
        donations_2 = filter_donations_by_tags([tag2])
        donations_1_2_3 = filter_donations_by_tags([tag1,tag2,tag3])
        assert len(donations_1_2) == 1
        assert donations_1_2[0].description == "1"
        assert len(donations_2_3) == 1
        assert donations_2_3[0].description == "2"
        assert len(donations_2) == 2
        assert len(donations_1_2_3) == 0

class RequestTest(MyTest):
    def test_add_request(self):
        donor = add_new_user(email="email1", name="donor_name", location="test_location2", password="test_password")
        donation = add_new_donation(user_email="email1", description='test', is_gluten_free=True,recipients_amount=4)
        recipient = add_new_user(email="email2", name="recipient_name", location="test_location2",
                             password="test_password")
        request = add_new_request(recipient=recipient.email,donor=donor.email,donation=donation.id,recipients_amount=2)
        assert request.id != None
        assert request.donation == donation.id
        assert request.donor == donor.email
        assert request.recipient == recipient.email

    def test_update_volunteer_to_request(self):
        donor = add_new_user(email="email11", name="donor_name", location="test_location2", password="test_password")
        donation = add_new_donation(user_email="email11", description='test', is_gluten_free=True, recipients_amount=4)
        volunteer = add_new_user(email="email33", name="name", location="test_location2", password="test_password")
        recipient = add_new_user(email="email22", name="recipient_name", location="test_location2",
                                 password="test_password")
        request = add_new_request(recipient=recipient.email, donor=donor.email, donation=donation.id,
                                  recipients_amount=2)
        update_volunteer(volunteer_id=volunteer.email,request_id=request.id)
        assert request.volunteer == volunteer.email

    def test_update_status_to_request(self):
        donor = add_new_user(email="email111", name="donor_name", location="test_location2", password="test_password")
        donation = add_new_donation(user_email="email111", description='test', is_gluten_free=True, recipients_amount=4)
        recipient = add_new_user(email="email222", name="recipient_name", location="test_location2",
                                 password="test_password")
        request = add_new_request(recipient=recipient.email, donor=donor.email, donation=donation.id,
                                  recipients_amount=2)
        update_request_in_process(request_id=request.id)
        assert request.status == RequestStatus.In_process.value
        update_request_Delivered(request_id=request.id)
        assert request.status == RequestStatus.Delivered.value

class FrequencyTest(MyTest):
    def test_frequency(self):
        recipient = add_new_user(email="recipient123", name="recipient_name", location="test_location2",
                                 password="test_password")
        donor = add_new_user(email="donor123", name="donor_name", location="test_location2", password="test_password")
        update_frequency(recipient_email="recipient123",donor_email="donor123")
        frequency = get_frequency(recipient_email="recipient123",donor_email="donor123")
        assert frequency.donor == "donor123"
        assert frequency.recipient == "recipient123"
        assert frequency.counter == 1
        update_frequency(recipient_email="recipient123", donor_email="donor123")
        frequency = get_frequency(recipient_email="recipient123", donor_email="donor123")
        assert frequency.donor == "donor123"
        assert frequency.recipient == "recipient123"
        assert frequency.counter == 2


if __name__ == '__main__':
    unittest.main()
