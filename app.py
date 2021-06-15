from flask import Flask, redirect, render_template, Blueprint
from flask_mail import Mail, Message

from DB import get_all_donations, get_all_tag_names, add_new_donation, del_all_donations, remove_from_blacklist
from DB.Suspicious import check_suspicious_users, remove_from_suspicious_list, get_all_suspicious_users, \
    add_to_Suspicious
from Demo import build_demo_donors, build_demo_donations, build_demo_tags, build_demo_requests
from server.home_page import home_page
from server.Donation_Creation import Donation_creation_page, list_to_string
from server.Donation_Preview import Donation_preview_page
from server.Login import login_page, set_session_data
from server.Register import Register_page
from server.log import log_page
from server.profile import profile_page
from server.Edit_Profile import edit_profile_page
from server.AdminView import AdminPage

from DB.users import *
import os

from DB.db_init import *
from apscheduler.schedulers.background import BackgroundScheduler

# config
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taumanyforone@gmail.com'
app.config['MAIL_PASSWORD'] = 'M21111994'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.register_blueprint(home_page)
app.register_blueprint(Donation_creation_page)
app.register_blueprint(Donation_preview_page)
app.register_blueprint(login_page)
app.register_blueprint(log_page)
app.register_blueprint(Register_page)
app.register_blueprint(profile_page)
app.register_blueprint(edit_profile_page)
app.register_blueprint(AdminPage)

db.init_app(app)

with app.app_context():
    # create database tables if they don't exist yet
    #db.drop_all()
    db.create_all()
    try:
        #build_demo_donors()
        #build_demo_donations()
        #build_demo_tags()
        #build_demo_requests()
        pass

    except Exception as e:
        print(e)


def do_periodically():
    with app.app_context():
        update_all_contribution_ranks()
        check_suspicious_users()
        pass


def schedule_periodic_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(do_periodically, 'interval', days=1)
    scheduler.start()
    do_periodically()


if __name__ == '__main__':
    app.before_first_request(schedule_periodic_tasks)

    '''
    uncomment depending on your environment - 
    '''
    #app.run() #for local running
    #app.run(host="delta-tomcat-vm.cs.tau.ac.il", port="40595") #for nova

