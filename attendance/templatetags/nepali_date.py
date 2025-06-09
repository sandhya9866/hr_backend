from django import template
import nepali_datetime

register = template.Library()

@register.filter
def to_nepali_date(value):
    if not value:
        return ""
    try:
        return nepali_datetime.date.from_datetime_date(value)
    except Exception:
        return ""
