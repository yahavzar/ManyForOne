from DB.db_init import *


class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    donor = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    counter = db.Column(db.Integer, nullable=False, default=0)


def update_frequency(recipient_email, donor_email):
    """
    :param recipient_email:
    :param donor_email:
    :return: frequency obj / general exception
    """
    # check if already in table
    frequency_obj = Frequency.query.filter_by(recipient=recipient_email, donor=donor_email).first()
    if frequency_obj:
        try:
            frequency_obj.counter += 1
            db.session.commit()
            return frequency_obj

        except Exception as e:
            db_logger.error("func: update_frequency failed with error %s" % e)
            raise e
    else:
        new_frequency_obj = Frequency(recipient=recipient_email, donor=donor_email, counter=1)
        try:
            db.session.add(new_frequency_obj)
            db.session.commit()
            return new_frequency_obj

        except Exception as e:
            db_logger.error("func: update_frequency failed with error %s" % e)
            raise e

def update_multi_frequency(recipient_email, donor_email,amount):
    """
    :param recipient_email:
    :param donor_email:
    :return: frequency obj / general exception
    """
    # check if already in table
    frequency_obj = Frequency.query.filter_by(recipient=recipient_email, donor=donor_email).first()
    if frequency_obj:
        try:
            frequency_obj.counter += amount
            db.session.commit()
            return frequency_obj

        except Exception as e:
            db_logger.error("func: update_frequency failed with error %s" % e)
            raise e
    else:
        new_frequency_obj = Frequency(recipient=recipient_email, donor=donor_email, counter=amount)
        try:
            db.session.add(new_frequency_obj)
            db.session.commit()
            return new_frequency_obj

        except Exception as e:
            db_logger.error("func: update_frequency failed with error %s" % e)
            raise e




def get_frequency(recipient_email, donor_email):
    """
    :param recipient_email:
    :param donor_email:
    :return: frequency obj / None
    """
    frequency_obj = Frequency.query.filter_by(recipient=recipient_email, donor=donor_email).first()
    return frequency_obj
