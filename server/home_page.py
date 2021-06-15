
from flask import request, Blueprint, render_template, url_for, redirect, session
from DB import *

from server.Login import clear_session_data

home_page = Blueprint('home', __name__, template_folder='../gui/templates')

@home_page.route('/', methods=['POST', 'GET'])
@home_page.route('/Home', methods=['POST', 'GET'])
def index():

    location_coordinate = str([34.766967, 32.085620])

    if 'email' in session:
        requests_list = Request.query.filter_by(recipient=session['email']).all()
        geojson = create_geojson(requests_list=requests_list)
        username = session['username']
        location = get_user(session['email']).location
        if location!= "":
            cordinate=get_coordinates(location)
            location=get_coordinates(location)
            if location==[]:
                location=0
            if cordinate!=[]:
                location_coordinate = cordinate
        return render_template("Home.html", username=username, input_json=geojson, location=location,
                               location_cordinate=location_coordinate,
                               radius=5000, top5=get_top_5_users(), tags=get_all_tag_names())
    geojson = create_geojson()
    return render_template("Home.html", input_json=geojson, radius=5000, top5=get_top_5_users(),
                           tags=get_all_tag_names(), location_cordinate=location_coordinate)


@home_page.route('/Logout')
def logout():
    # remove the username from the session if it is there
    clear_session_data()
    return redirect(url_for('home.index'))


@home_page.route('/filter', methods=['POST', 'GET'])
def filter_map():
    if 'email' not in session:
        return redirect("\Login")
    if request.method == 'POST':
        form = request.form

        # location
        radius = form.get('radius')
        if not radius.isnumeric():
            radius = 5000
        location = form.get('location')
        if location != '':
            cordinate = get_coordinates(location)
            if cordinate != []:
                location_coordinate = cordinate
                location=cordinate
            else:
                location_coordinate = 0

        else:
            location_coordinate = 0

        if location_coordinate == 0:
            if 'email' in session:
                cordinate= get_coordinates(get_user(session['email']).location)
                if cordinate != []:
                    location_coordinate = cordinate
                    location=cordinate
                else:
                    location_coordinate = str([34.766967, 32.085620])
                    location=0

        if 'email' in session:
            requests_list = Request.query.filter_by(recipient=session['email']).all()
            geojson = create_geojson(filter_dict=form, requests_list=requests_list)
            username = session['username']
            return render_template("Home.html", username=username, input_json=geojson, radius=radius,
                                   location=location, location_cordinate=location_coordinate,
                                   top5=get_top_5_users(), tags=get_all_tag_names())

        geojson = create_geojson(filter_dict=form)
        return render_template("Home.html", input_json=geojson, radius=radius, location=location,
                               top5=get_top_5_users(), tags=get_all_tag_names(), location_cordinate=location_coordinate)
