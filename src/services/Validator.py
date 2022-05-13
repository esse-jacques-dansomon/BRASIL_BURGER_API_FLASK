import validators
import re

from src.models.Client import Client
from src.models.User import User


class validator_data:
    erros = []

    def __init__(self):
        self.errors = {}

    def is_unique_username(self, username):
        if User.query.filter_by(username=username).first() or self.empty_validator(username):
            self.errors['username'] = "Username is already used"

    def is_unique_phone(self, number):
        if Client.query.filter_by(phone=number).first():
            self.errors['number'] = "Phone number is already used"

    def is_unique_mail(self, email):
        if self.empty_validator(email) or User.query.filter_by(email=email).first():
            self.errors['email'] = "Email is already used"

    def validate_email(self, email):
        if not validators.email(email):
            self.errors['email'] = "Email is not valid"
        else:
            self.is_unique_mail(email)

    def senegal_number_validator(self, number):
        """
        Validates Senegal phone numbers.
        """
        # number = number.replace(" ", "")
        try:
            int(number)
            regex = re.compile(r'^(77|78|75|70|76)[0-9]{7}$')
            if not regex.match(number):
                self.errors['number'] = "Phone number is not valid"
            else:
                self.is_unique_phone(number)
        except ValueError:
            self.errors['number'] = "Phone number is not valid"

    def empty_validator(self, field):
        return field == "" or field is None or field == " "

    def is_validated(self):
        return len(self.errors) == 0

    def get_errors(self):
        return self.errors
