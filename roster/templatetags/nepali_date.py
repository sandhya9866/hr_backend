# your_app/templatetags/nepali_date.py

from django import template
from utils.date_converter import english_to_nepali

register = template.Library()

@register.filter
def to_nepali_date(value):
    return english_to_nepali(value)
