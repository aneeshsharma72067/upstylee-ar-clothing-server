from validate_email_address import validate_email
from re import match

def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return validate_email(email) and match(email_pattern, email) is not None


def is_valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()
