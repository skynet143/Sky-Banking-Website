# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='hide_digits')
def hide_digits(value):
    value_str = str(value)
    hidden_part = '*' * (len(value_str) - 4)
    visible_part = value_str[-4:]
    return hidden_part + visible_part
