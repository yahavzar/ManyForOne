import os

from flask import  Blueprint, render_template, session, request, redirect
from werkzeug.utils import secure_filename

from DB import get_user, update_user_details

edit_profile_page = Blueprint('EditProfile', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static_files'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg','gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@edit_profile_page.route('/EditProfile', methods=['POST', 'GET'])
def index():
    if 'email' not in session:
        return redirect("/Login")
    return render_template("EditProfile.html", request=request)


@edit_profile_page.route('/ChangeDetails', methods=['POST', 'GET'])
def change_details():
    if 'email' not in session:
        return redirect("/Login")
    if request.method == 'POST':
        password = request.form.get("Password")
        location = request.form.get("Location")
        status = request.form.get("Status")
        img_path=""
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
                        img_path = "%s_%s" % (img_path, c)
                        c += 1
                    abs_path = os.path.abspath(img_path)
                    file.save(abs_path)
        update_details(session['email'], password, location, status,img_path)

    return redirect("/Profile")


def update_details(email, password, location, status,img_path):
    # Get current user
    user = get_user(email)
    if len(password)<8:
        password=user.password
    if location=="":
        location=user.location
    if status=="":
        status=user.status_text
    if img_path=="":
        img_path=user.picture
    # Change details
    update_user_details(email, password, location, status,img_path)

