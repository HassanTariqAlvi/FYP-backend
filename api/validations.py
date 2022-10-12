import re
from rest_framework.serializers import ValidationError


def validate_name(value):
    if not re.match('[a-zA-Z\s]+$', value):
        raise ValidationError('This field must contain only alphabets')
    return value


def validate_positive_number(value):
    if value < 0:
        raise ValidationError('Invalid number. Must be a positive number')
    return value


def validate_phone_no(value):
    if not value.isdigit():
        raise ValidationError(
            'Phone no must contain only digits')
    if len(value) < 11:
        raise ValidationError('Phone no must be of 11 digits')
    return value


def validate_city(value):
    if not re.match('[a-zA-Z\s]+$', value):
        raise ValidationError(
            'City must contain only alphabets')
    return value


def validate_cnic(value):
    if not value.isdigit():
        raise ValidationError('CNIC must contain only digits')
    if len(value) < 13:
        raise ValidationError('CNIC must be of 13 digits')
    return value
