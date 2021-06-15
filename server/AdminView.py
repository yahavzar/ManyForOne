from flask import request, render_template, Blueprint, session, jsonify, redirect
from DB import get_all_blacklisted_users, get_user_donations, get_all_requests_by_user, get_all_requests_by_donor
from DB.Suspicious import get_all_suspicious_users, remove_from_suspicious_list
from DB.blacklist import add_to_blacklist, remove_from_blacklist
import json

AdminPage = Blueprint('AdminPage', __name__, template_folder='../templates')


@AdminPage.route('/Admin', methods=['POST', 'GET'])
def index():
    if "email" not in session or session["email"] !="taumanyforone@gmail.com":
        return redirect("/")
    if request.method == "POST":
        table = request.form.get('data')
        table1 = request.form.get('data1')
        if table is not None:
            suspicious_table_rows = json.loads(table)
            for row in suspicious_table_rows:
                if 'update' in row:
                    # Remove from suspicious list
                    remove_from_suspicious_list(row['email'])
                    # Insert to blacklist
                    add_to_blacklist(row['email'])
        if table1 is not None:
            blacklist_table_rows = json.loads(table1)
            for row in blacklist_table_rows:
                if 'update1' in row:
                    # Remove from blacklist
                    remove_from_blacklist(row['email1'])
                    donations = get_user_donations(row['email1'])
                    requests1 = get_all_requests_by_user(row['email1'])
                    requests2 = get_all_requests_by_donor(row['email1'])
    blacklistedUsers = []
    suspiciousUsers = []
    for suspiciousUser in get_all_suspicious_users():
        suspiciousUsers.append({"email": suspiciousUser})
    for blacklistedUser in get_all_blacklisted_users():
        blacklistedUsers.append({"email1": blacklistedUser})


    return render_template("admin-view.html", suspiciousList=suspiciousUsers, blacklist=blacklistedUsers)
