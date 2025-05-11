from django import template

register = template.Library()

@register.filter
def dividedby(value, arg):
    return value / arg
