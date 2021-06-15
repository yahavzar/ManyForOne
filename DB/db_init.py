from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from utils.logging_utils import *

db = SQLAlchemy()
db_logger = setup_logger(name="DB_Logger", log_path="db.log")


#######################   Relationships  #################################

#### One-to-Many
# 1 user -> many donations


#### Many-to-Many
# many donations <-> many tags


#########################  DB ERRORS #####################################

class DBError(Exception):
    """Base class for other db exceptions"""
    def __init__(self, message):
        self.message = message
    pass

class EmailExistsInDB(DBError):
    """Raised when there is an attempt to add a new user with the same email"""
    pass

class RecipientsAmountTooBig(DBError):
    """Raised when recipients_amount > donation.recipients_amount"""
    pass
