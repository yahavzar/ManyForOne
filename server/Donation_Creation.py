from flask import Flask, Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

from DB import db_init
from DB.donations import *
from DB.users import *

Donation_creation_page = Blueprint('DonationCreation', __name__, template_folder='../templates')
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static_files'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
IMAGE = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@Donation_creation_page.route('/newDonation', methods=['POST', 'GET'])
def index():
    if 'email' not in session:
        return redirect("/Login")

    return render_template("DonationCreation.html")


@Donation_creation_page.route('/createDonation', methods=['POST', 'GET'])
def createDonation():
    if request.method == 'POST':
        description = request.form.get("Description")
        quantity = request.form.get("Quantity")
        kosher = request.form.get("Kosher")
        meat = request.form.get("Meat")
        dairy = request.form.get("Dairy")
        vegan = request.form.get("Vegan")
        gluten = request.form.get("GlutenFree")
        # Checking if images were uploaded
        if 'donation_images' not in session:
            images = ["../static/images/BurgerDonation.png"]
        else:
            images = session['donation_images']

        labels = ""
        if kosher is not None:
            labels += "Kosher, "
            kosher = True
        else:
            kosher = False
        if meat is not None:
            labels += "Meat, "
            meat = True
        else:
            meat = False
        if dairy is not None:
            labels += "Dairy, "
            dairy = True
        else:
            dairy = False
        if vegan is not None:
            labels += "Vegan, "
            vegan = True
        else:
            vegan = False
        if gluten is not None:
            labels += "Gluten free"
            gluten = True
        else:
            gluten = False

        if labels != "" and labels[len(labels) - 1] == " ":
            labels = labels[:len(labels) - 2]

        try:
            images_str = list_to_string(images)
            user = get_user(session['email'])
            email = user.email
            add_new_donation(user_email=email, recipients_amount=quantity, is_predictable=False,
                             description=description, picture=images_str, start_time=None,
                             end_time=None, is_open=True, is_in_process=False,
                             is_kosher=kosher, is_vegan=vegan, is_meat=meat, is_dairy=dairy, is_gluten_free=gluten)

        except db_init.EmailExistsInDB:
            render_template("Error.html")

        return redirect('/')
    return redirect('/')


@Donation_creation_page.route('/addImage', methods=['POST', 'GET'])
def addImage():
    if 'email' not in session:
        return redirect("/Login")
    # Clean images array
    images = []
    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        for file in files:
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename != '':
                upload_folder = r'static/donations_pictures'
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    img_path = "%s/%s" % (upload_folder, filename)
                    c = 0
                    while os.path.exists(img_path):
                        img_path = "%s_%s" % (img_path, c)
                        c += 1
                    abs_path = os.path.abspath(img_path)
                    file.save(abs_path)
                    img_path = "../" + img_path
                    images.append(img_path)

        session['donation_images'] = images
        return render_template("DonationCreation.html", images=images)

    return render_template("DonationCreation.html", images="../static/images/BurgerDonation.png")



def list_to_string(list):
    return_str = ""
    for i in range(len(list)):
        if i == len(list):
            return_str += list[i]
        else:
            return_str += list[i] + ","
    return return_str
