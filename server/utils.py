import mapbox
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taumanyforone@gmail.com'
app.config['MAIL_PASSWORD'] = 'M21111994'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
API_KEY = 'pk.eyJ1IjoieWFoYXZ6YXJmYXRpIiwiYSI6ImNrbnZ1NnkyZzBxYWYycXJ2ZTEyMGR1eTYifQ.B4LS0v9ClG3yiF0mn3TGLA'


def send_mail(title, body, recipients, sender="taumanyforone@gmail.com"):
    try:
        with app.app_context():
            msg = Message(title, sender=sender, recipients=recipients)
            msg.body = body
            mail.send(msg)
        return True
    except:
        return False


def get_coordinates(address):
    """
    :param address:
    :return: coordinates_list
    """
    Geocoder = mapbox.Geocoder(access_token=API_KEY)
    req_obj = Geocoder.forward(address=address, country=['il'], limit=1)
    geojson = req_obj.geojson()
    if len(geojson['features']) > 0:
        coordinates_list = geojson['features'][0]['geometry']['coordinates']
        return coordinates_list
    return list()
