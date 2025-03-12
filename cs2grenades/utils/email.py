import re


def email_validator(email):
    """
    Return True if e-mail is valid \n
    Return False if e-mail is invalid
    """
    valid_email = re.compile(
        r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", re.IGNORECASE)
    return valid_email.match(email)
