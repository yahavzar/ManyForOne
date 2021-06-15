import collections
import difflib
import statistics
import threading

from DB.donations import *
from DB.tagging import *
from DB.users import get_user, update_tagging_score, update_suspicious_requests_today, get_suspicious_requests_today
from fuzzywuzzy import fuzz
import haversine as hs

from flask import redirect, Flask, Blueprint, render_template, request, session
from DB import donations, add_new_request, RequestStatus, get_all_volunteer_requests_of_donation, \
    volunteer_taking_a_request, get_request
from server.utils import send_mail

Donation_preview_page = Blueprint('Donation-Preview', __name__, template_folder='../templates')
TAGGING_BAR = 5
SIMILAR_TAGS_COUNTER = 3
SUSPICIOUS_TIME = 2


@Donation_preview_page.route('/Donations/<donation_id>', methods=['GET'])
def index(donation_id):
    login = "false"
    if 'email' in session:
        login = "ture"
        session['user_suggested_tag'] = None
    donation_obj = donations.get_donation(donation_id)
    id = donation_obj.id
    donor = donations.get_donor(donation_id)
    title = donor.name.title()
    location = donor.location.title()
    description = donation_obj.description
    quantity = donation_obj.recipients_amount - donation_obj.taken_quantity
    labels = donations.get_donation_labels(donation_id)
    tags = ", ".join([tag.name for tag in donation_obj.tags])
    if len(tags) > 1:
        labels = "%s, %s" % (labels, tags)
    images = donations.get_donation_image(donation_id)
    images_list = images.split(",")
    if images_list[len(images_list) - 1] == "":
        images_list.pop()
    addQuantity = 0
    if donation_obj.is_predictable == True and 'email' in session and session['email'] not in \
            donation_obj.quantity_predictions['Users']:
        addQuantity = 1
        if len(donation_obj.quantity_predictions['Predictions']) == 0:
            quantity = "Please suggest Quantity"
    return render_template("Donation-Preview.html", donation_id=id, title=title, description=description,
                           quantity=quantity, labels=labels, location=location, images=images_list, similar_tags=[],
                           login=login, addQuantity=addQuantity)


@Donation_preview_page.route('/get-requests', methods=['POST', 'GET'])
def index2():
    if request.method == "POST":
        table_rows = json.loads(request.form.get('data'))
        for row in table_rows:
            if row['status'] == 'Take delivery':
                volunteer_taking_a_request(volunteer_id=session['email'], request_id=row['id'])
                request_object = get_request(row['id'])
                args = ("Someone took your request",
                        "We are happy to inform you that there is a volunteer to collect your request.",
                        [request_object.recipient],)
                threading.Thread(target=send_mail, args=args).start()
                args = ("Status Update",
                        "We are happy to inform you that there is a volunteer to collect a donation from you.",
                        [request_object.donor],)
                threading.Thread(target=send_mail, args=args).start()


    donation_id = session["shown_donation_id"]
    session["shown_donation_id"] = None
    return redirect('/Donations_Requests/%s' % donation_id)


@Donation_preview_page.route('/Donations_Requests/<donation_id>', methods=['GET'])
def index1(donation_id):
    # Must be logged in to perform this action
    login = "false"
    if 'email' in session:
        login = "ture"

    donation_obj = donations.get_donation(donation_id)
    # donation info
    id = donation_obj.id
    donor = donations.get_donor(donation_id)
    title = donor.name.title()
    location = donor.location.title()
    description = donation_obj.description
    quantity = donation_obj.recipients_amount - donation_obj.taken_quantity
    labels = donations.get_donation_labels(donation_id)
    tags = ", ".join([tag.name for tag in donation_obj.tags])
    if len(tags) > 1:
        labels = "%s, %s" % (labels, tags)
    images = donations.get_donation_image(donation_id)
    images_list = images.split(",")
    if images_list[len(images_list) - 1] == "":
        images_list.pop()

    # list of requests
    rows = []
    requests = get_all_volunteer_requests_of_donation(donation_obj.id)
    for request_obj in requests:
        recipient = get_user(request_obj.recipient)
        loc_recipient = eval(recipient.coordinates)
        loc_donor = eval(donor.coordinates)
        km_distance = hs.haversine(loc_recipient, loc_donor)
        recipient_location = recipient.location.title()
        quantity = request_obj.recipients_amount
        id = request_obj.id
        rows.append({"id": id, "recipient_location": recipient_location, "quantity": quantity, "distance": km_distance})

    session["shown_donation_id"] = donation_id
    return render_template("Donation-Preview-Requests.html", donation_id=id, title=title, description=description,
                           quantity=quantity, labels=labels, location=location, images=images_list, res=rows,
                           login=login)


@Donation_preview_page.route('/similarTag/<donation_id>', methods=['POST', 'GET'])
def similarTag(donation_id):
    # Must be logged in to perform this action
    if 'email' not in session:
        return redirect("/Login")

    donation_obj = donations.get_donation(donation_id=donation_id)
    id = donation_obj.id
    donor = donations.get_donor(donation_id=donation_id)
    title = donor.name.title()
    location = donor.location.title()
    description = donation_obj.description
    quantity = donation_obj.recipients_amount
    labels = donations.get_donation_labels(id=donation_id)
    images = donations.get_donation_image(id=donation_id)
    images_array = images.split(',')
    addQuantity = 0
    if donation_obj.is_predictable == True and 'email' in session and session['email'] not in \
            donation_obj.quantity_predictions['Users']:
        addQuantity = 1
        if len(donation_obj.quantity_predictions['Predictions']) == 0:
            quantity = "Please suggest Quantity"
    if request.method == 'POST':
        suggested_tag_str = request.form.get("Label")
        if suggested_tag_str is None or suggested_tag_str == "":
            return redirect("/Donations/%s" % donation_id)

        suggested_tag_str = suggested_tag_str.lower()
        suggested_tags_dict = donation_obj.suggested_tags
        session['user_suggested_tag'] = suggested_tag_str

        similar_tags_list = get_similar_tags(suggested_tag_str, suggested_tags_dict)
        for i in range(3 - len(similar_tags_list)):
            similar_tags_list.append(None)
        if suggested_tag_str in similar_tags_list:
            user_suggested_tag = None
        else:
            user_suggested_tag = session['user_suggested_tag']


        session['similar_tags_list'] = similar_tags_list
        return render_template("Donation-Preview.html", donation_id=id, title=title, description=description,
                               quantity=quantity, labels=labels, location=location, images=images_array, flag=1,
                               similar_tags_flag=1, similar_tags=similar_tags_list,
                               user_suggested_tag=user_suggested_tag, addQuantity=addQuantity)

    return render_template("Donation-Preview.html")


@Donation_preview_page.route('/chosenTags/<donation_id>', methods=['POST', 'GET'])
def chosenTag(donation_id):
    if 'email' not in session:
        return redirect("/Login")
    if request.method == 'POST':
        donation_obj = donations.get_donation(donation_id)
        similar_tags = session['similar_tags_list']
        similar_tags.append(session['user_suggested_tag'])
        tag1 = request.form.get("Tag1")
        tag2 = request.form.get("Tag2")
        tag3 = request.form.get("Tag3")
        tag4 = request.form.get("Tag4")
        tags_arr = [tag1, tag2, tag3, tag4]
        for i in range(len(tags_arr)):
            if tags_arr[i] is not None:
                tag_to_add = similar_tags[i]
                handle_new_suggested_tag(donation_id, tag_to_add)
                donation_obj = donations.get_donation(donation_id)

        session['similar_tags_list'] = None

    return redirect("/Donations/%s" % donation_id)


@Donation_preview_page.route('/newLabel/<donation_id>', methods=['POST', 'GET'])
def newLabel(donation_id):
    # Must be logged in to perform this action
    if 'email' not in session:
        return redirect("/Login")

    if request.method == 'POST':
        new_tag = request.form.get("Label")
        if new_tag is None or new_tag == "":
            return redirect("/Donations/%s" % donation_id)
        new_tag = new_tag.lower()

        handle_new_suggested_tag(donation_id, new_tag)

    return redirect("/Donations/%s" % donation_id)


def handle_new_suggested_tag(donation_id, new_tag, user_email=""):
    donation_obj = donations.get_donation(donation_id=donation_id)
    if any([new_tag == tag.name for tag in donation_obj.tags]):
        # Tag already exists for this donation
        return

    suggested_tags_dict = json.loads(json.dumps(dict(donation_obj.suggested_tags)))
    if user_email == "":
        user_email = session['email']

    user = get_user(user_email)
    user_tagging_score = user.tagging_score
    if new_tag in suggested_tags_dict:
        if user_email not in suggested_tags_dict[new_tag]["user_ids"]:
            suggested_tags_dict[new_tag]["sum"] += user_tagging_score
            suggested_tags_dict[new_tag]["user_ids"].append(user_email)
    else:
        suggested_tags_dict[new_tag] = {"sum": user_tagging_score, "user_ids": [user_email]}

    donation_obj.suggested_tags = suggested_tags_dict
    if suggested_tags_dict[new_tag]["sum"] >= TAGGING_BAR:
        # the tag can be added to the donation
        # remove from suggestions
        tag_dict = suggested_tags_dict.pop(new_tag)
        donation_obj.suggested_tags = suggested_tags_dict
        db.session.commit()

        # add to donation
        tag_obj = get_or_add_tag(new_tag)
        add_tag_to_donation(donation_obj, tag_obj)
        db.session.commit()

        # update users
        users_to_update = tag_dict["user_ids"]
        for user_id in users_to_update:
            user = get_user(user_id)
            update_tagging_score(user_id)

    db.session.commit()


@Donation_preview_page.route('/addQuantity/<donation_id>', methods=['POST', 'GET'])
def addQuantity(donation_id):
    if 'email' not in session:
        return redirect("/Login")
    if request.method == 'POST':
        quantity = request.form.get("Quantity")
    donation_obj = donations.get_donation(donation_id)
    if donation_obj.is_predictable == True:
        quantity_predictions_dict = get_quantity_predictions_dict(donation_id)
        if session['email'] not in quantity_predictions_dict['Users']:
            quantity_predictions_dict['Users'].append(session['email'])
            quantity_predictions_dict['Predictions'].append(int(quantity))
            donation_obj.recipients_amount = int(statistics.median(quantity_predictions_dict['Predictions']))
            if (donation_obj.recipients_amount - donation_obj.taken_quantity) < 1:
                donation_obj.recipients_amount = 0
                donation_obj.is_open = False
            db.session.commit()
            save_quantity_predictions_dict(donation_id, quantity_predictions_dict)
    return redirect("/Donations/%s" % donation_id)


def get_similar_tags(tag_string, suggested_tags_dict):
    suggested_tags = suggested_tags_dict.keys()
    existing_tags = get_all_tag_names()
    all_tags = existing_tags + list(set(suggested_tags) - set(existing_tags))
    similar_tags_substring = get_similar_tags_substring(tag_string, all_tags)
    similar_tags_sequence = get_similar_tags_sequence(tag_string, all_tags)
    similar_tags_fuzzy = get_similar_tags_fuzzy(tag_string, all_tags)
    results = list(similar_tags_substring + similar_tags_sequence + similar_tags_fuzzy)
    most_common = [tup[0] for tup in collections.Counter(results).most_common(SIMILAR_TAGS_COUNTER)]
    return most_common


def get_similar_tags_sequence(tag_string, all_tags, top_matches=3):
    results = []
    top_matched_tags = []
    for tag in all_tags:
        seq = difflib.SequenceMatcher(None, tag, tag_string)
        ratio = seq.ratio() * 100
        results.append((tag, ratio))
    sorted_by_ratio = sorted(results, key=lambda tup: tup[1], reverse=True)
    for tup in sorted_by_ratio[:top_matches]:
        top_matched_tags.append(tup[0])
    return top_matched_tags


def get_similar_tags_substring(tag_string, all_tags):
    results = []
    for tag in all_tags:
        if tag in tag_string:
            results.append(tag)
    return results


# Returns array of the 3 most similar tags
def get_similar_tags_fuzzy(tag_string, all_tags):
    similar_tags = []
    try:
        check_tag = tag_string.lower()
        similar_tags = []
        min_tag_ratio = ""
        min_tag_index = 0

        for tag in all_tags:
            ratio = fuzz.token_sort_ratio(tag.lower(), check_tag)

            # Similar tag list is empty
            if len(similar_tags) == 0:
                min_tag_index = 0
                min_tag_ratio = ratio
            # Less than 3 similar tags
            if len(similar_tags) < 3:
                similar_tags.append(tag)
                if ratio < min_tag_ratio:
                    min_tag_ratio = ratio
                    min_tag_index = len(similar_tags)
            # Similar tag list is full (3 tags) need to switch 1 tag if ratio is smaller
            else:
                # Check if the ratio of the new tag is bigger than the minimum ratio so far
                if ratio > min_tag_ratio:
                    similar_tags[min_tag_index] = tag
                    # Need to update minimum ratio and index now. Find minimum ratio first
                    min_ratio = 100
                    for similar_tag in similar_tags:
                        if fuzz.token_sort_ratio(check_tag, similar_tag.lower()) < min_ratio:
                            min_ratio = fuzz.token_sort_ratio(check_tag, similar_tag)
                    min_tag_ratio = min_ratio
                    # Now find index
                    tag_index = 0
                    for i in range(len(similar_tags)):
                        if fuzz.token_sort_ratio(similar_tags[i], check_tag) == min_ratio:
                            tag_index = i
                    min_tag_index = tag_index
    except Exception as e:
        print("get_similar_tags_fuzzy: %s" % e)
    return similar_tags


@Donation_preview_page.route('/takeorder/<donation_id>', methods=['POST', 'GET'])
def choseMethod(donation_id):
    if 'email' not in session:
        return redirect("/Login")
    if request.method == 'POST':
        donation_obj = donations.get_donation(donation_id)
        quantity = request.form.get("Quantity")
        method = request.form.get("Method")
        donor_email = get_donor(donation_id).email
        # if the person that requested the donation is the one that created it

        if session['email'] == donor_email:
            id = donation_obj.id
            donor = donations.get_donor(donation_id)
            title = donor.name.title()
            location = donor.location.title()
            description = donation_obj.description
            quantity = donation_obj.recipients_amount - donation_obj.taken_quantity
            labels = donations.get_donation_labels(donation_id)
            donation_tags = ", ".join([tag.name for tag in donation_obj.tags])
            if len(donation_tags) > 1:
                labels = "%s, %s" % (labels, donation_tags)
            images = donations.get_donation_image(donation_id)
            images_list = images.split(",")
            if images_list[len(images_list) - 1] == "":
                images_list.pop()
            addQuantity = 0
            if donation_obj.is_predictable == True:
                if len(donation_obj.quantity_predictions['Predictions']) == 0:
                    quantity = "Please suggest Quantity"
                addQuantity = 1

            return render_template("Donation-Preview.html", donation_id=id, title=title, description=description,
                                   quantity=quantity, labels=labels, location=location, images=images_list,
                                   error_donations_request_flag="true", addQuantity=addQuantity)

        # Check if donation was requested in an unusual time (too fast)
        diff_time = datetime.utcnow() - donation_obj.start_time
        recipient_email = session['email']

        if diff_time.total_seconds() < SUSPICIOUS_TIME:
            update_suspicious_requests_today(recipient_email)

        if donation_obj.is_predictable and len(donation_obj.quantity_predictions['Predictions']) == 0:
            id = donation_obj.id
            donor = donations.get_donor(donation_id)
            title = donor.name.title()
            location = donor.location.title()
            description = donation_obj.description
            quantity = donation_obj.recipients_amount - donation_obj.taken_quantity
            labels = donations.get_donation_labels(donation_id)
            donation_tags = ", ".join([tag.name for tag in donation_obj.tags])
            if len(donation_tags) > 1:
                labels = "%s, %s" % (labels, donation_tags)
            images = donations.get_donation_image(donation_id)
            images_list = images.split(",")
            if images_list[len(images_list) - 1] == "":
                images_list.pop()
            if donation_obj.is_predictable == True:
                if len(donation_obj.quantity_predictions['Predictions']) == 0:
                    quantity = "Please suggest Quantity"
                addQuantity = 1

            return render_template("Donation-Preview.html", donation_id=id, title=title, description=description,
                                   quantity=quantity, labels=labels, location=location, images=images_list,
                                   error=1, addQuantity=addQuantity)

        if method == 'TakeAway':
            add_new_request(recipient=session['email'], donation=donation_id, recipients_amount=int(quantity),
                            donor=donor_email)

            args = ("A new request has been received",
                    "We would like to update you that " + quantity + " meals has been requested from your donation.\nThe recipient will pick them up.",
                    [donor_email],)
            threading.Thread(target=send_mail, args=args).start()



        if method == "Delivery":
            add_new_request(recipient=session['email'], donation=donation_id, recipients_amount=int(quantity),
                            donor=donor_email, status=RequestStatus.By_volunteer.value)

            args = ("A new request has been received",
                    "We would like to update you that " + quantity + " meals has been requested from your donation.\nThe request is waiting for a volunteer to pick up the donation.",
                    [donor_email],)
            threading.Thread(target=send_mail, args=args).start()



    return redirect("/Donations/%s" % donation_id)
