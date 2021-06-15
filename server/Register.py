import threading

from flask import request, redirect,  session
from flask import Flask, Blueprint, render_template
from werkzeug.utils import secure_filename
import os
from DB import db_init
from DB.users import *
from DB.blacklist import get_all_blacklisted_users
from server.utils import send_mail

Register_page = Blueprint('Register', __name__, template_folder='../templates')
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static_files'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@Register_page.route('/Register', methods=['POST', 'GET'])
def index():
    if 'email'  in session:
        return redirect("/")
    return render_template("Register.html")


@Register_page.route('/Registration', methods=['POST', 'GET'])
def Register():
    if 'email'  in session:
        return redirect("/")
    if request.method == 'POST':
        username = request.form.get("UserName")
        Email = request.form.get("Email").lower()
        # Check if email is blacklisted
        blacklisted_users = get_all_blacklisted_users()
        if Email in blacklisted_users:
            return render_template("Register.html",blacklist_email=1)

        Password = request.form.get("Password")
        location = request.form.get("Location")
        img_path = None
        if 'file' in request.files:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename != '':
                upload_folder = r'static/profile_pictures'
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    img_path = "%s/%s" % (upload_folder, filename)
                    c = 0
                    while os.path.exists(img_path):
                        img_path = "%s_%s" % (img_path,c)
                        c += 1
                    abs_path = os.path.abspath(img_path)
                    file.save(abs_path)
        try:
            add_new_user(email=Email, name=username, location=location, password=Password, picture=img_path)
        except db_init.EmailExistsInDB:
            return render_template("Register.html",flag=1)
        args = ("Hi "+username+", Welcome to ManyforOne!",
                "\t\t\t\t WELCOME! \n\n"
                "We greatly appreciate your registration!\n"
                "In this site you can find food donations, add donations of your own or volunteer to deliver donations "
                "to users who can't pick them up themselves.\n"
                "\nDon't have donations? you can still help! Tag the donations and suggest quantities where needed to "
                "help users find the donations easily.\n"
                "\nAny contribution to the website is appreciated. Each day the top 5 contributors are published in the main page!\n"
                "\nYou can find a guide below, please contact us if you have any questions!\n"
                "\n\n\t\t      A Guide To The Website\n\t\t      ====================\n\n"
                "\t< Finding A Donation >\n\t -----------------------------------\n"
                "The map in the home page will show you the currently open donation.\n"
                "Donations in a radius of 5000 meters from your location will appear in red.\n"
                "\nAre you in a different location? enter your current address into the 'Update location' filed.\n"
                "Interested in other radius? enter the desire distance in the meters into the 'Radius search' field.\n"
                "\nYou can also filter the map with the buttons above it. "
                "In addition, you can filter it by choosing from the list of tags (hold Ctrl to choose more than one).\n"
                "Click 'Update Map' to see the donations that match your filters.\n"
                "\nIf you took a donation before, try the 'Show Recommendations' as well "
                "to see donations that you might like based on the donations you took before.\n"
                "\nFound a donation you like? Great!\n"
                "In the donation window choose 'Take it'.\n"
                "If you intend to take the donation yourself, pick 'Take Away' and enter the quantity you are going to collect. "
                "(You might need to suggest a quantity if there isn't one already).\n"
                "If you can't take the donation yourself, pick 'Delivery' and a volunteer might pick it up for you.\n"
                "\nGot the donation? please confirm & rate in the log page through your profile. "
                "If the donation is missing, please report it in the log page to help us keep a reliable process.\n"
                "\n\t< Adding A Donation >\n\t -----------------------------------\n"
                "Do you have food to donate? That's great! \nPlease click on the 'Add Donation' button above the map.\n"
                "You can add photos, description and tags to help users find your donation.\nThank you for your contribution!\n"
                "\n\t< Volunteering >\n\t -------------------------\n"
                "Can you deliver a donation from the donor? that's a great help!\n"
                "Pick 'Volunteer view' above the map and set the distance filters if needed, then click 'update map'.\n"
                "In the donation window, you can see all the requests to this donation."
                "\nIf you find a request you can take, choose 'Take delivery' under the 'Take it' column.\n"
                "Thank you for your contribution!\n"
                "\n\t< Tagging >\n\t ------------------\n"
                "Can you add Tags and quantities to donations? that's a great help!\n"
                "Pick 'Tagger view' above the map, then click 'update map'.\n"
                "\nIn the donation window you can see photos or description. "
                "If you have a new label to add that can describe the food, click 'Add Lable'.\n"
                "Before adding your label, you can check if there are already similar tags you can add.\n"
                "Existing tags are always preferable, but don't hesitate to add a new one where needed!\n"
                "\nYou added a label but don't see it in the donation window yet? that's ok! \n"
                "After a few more users will add this label too it will show up.\n "
                "The more good tags you add, the more weight your future tags will have! "
                "Like a rank in a game, we trust our pro-taggers :)\n"
                "\nOne more way to help is by predicting the numbers of users that can enjoy the donation.\n"
                "If you see the 'suggest quantity' button that means we need your help to predict the number of recipients.\n"
                "Can you suggest a quantity based on the photos? please click the button and enter your suggestion.\n"
                "Thank you for your contribution!\n",
                [Email],)
        threading.Thread(target=send_mail, args=args).start()
        return redirect("/Login")

    return render_template("profile.html")


