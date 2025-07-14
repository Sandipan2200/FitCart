from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='inr')
def inr(value):
    """Convert a number to INR format with ₹ symbol"""
    try:
        number = float(value)
        return f"₹{number:,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiply the given value by the argument"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, InvalidOperation):
        return 0
