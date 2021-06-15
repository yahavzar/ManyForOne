from flask import  Blueprint, render_template, session, redirect
from DB import get_user, get_status_of_user

profile_page = Blueprint('Profile', __name__, template_folder='../templates')


@profile_page.route('/Profile', methods=['POST', 'GET'])
def index():
    if "email" not in session :
        return redirect("/")
    email = session['email']
    user = get_user(email)
    username = user.name
    password = user.password
    location = user.location
    profileImage = user.picture
    status = user.status_text

    image = profileImage
    if image is None:
        image = "../static/images/user.png"
    else:
        image = get_profile_image(image)

    # Check if admin
    admin = 0
    if email.lower() == "taumanyforone@gmail.com":
        admin = 1
    donor, volunteer, recipient=get_status_of_user(email)
    return render_template("ProfilePage.html", image=image, username=username,
                           email=email, password=password, location=location, status=status, donor=donor, volunteer=volunteer,
                           recipients=recipient, admin=admin)


def get_profile_image(image):
    profile_image = "../" + image
    return profile_image
