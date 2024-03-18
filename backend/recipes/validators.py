import re

from django.core.exceptions import ValidationError

from backend.constants import HEX_FIELD_REQ, MAX_IMG_SIZE, SLUG_FIELD_REQ


def validate_hex_color(value):
    hex_reg = re.compile(HEX_FIELD_REQ)
    if not re.search(hex_reg, value):
        raise ValidationError("See the ReDoc for the hex field requirements.")


def validate_slug_field(value):
    slug_reg = re.compile(SLUG_FIELD_REQ)
    if not re.search(slug_reg, value):
        raise ValidationError("Check the ReDoc for the slug field requirements.")


def validate_img_size(image):
    max_lim = MAX_IMG_SIZE * 1024 * 1024
    if image.file.size > max_lim:
        raise ValidationError(f"The image must be <={MAX_IMG_SIZE}Mb in size.")
