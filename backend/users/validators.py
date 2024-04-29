import regex as re

from backend.constants import USERNAME_FIELD_REQ


def validate_username_field(value):
    username_reg = re.compile(USERNAME_FIELD_REQ)
    return re.search(username_reg, value) is None
