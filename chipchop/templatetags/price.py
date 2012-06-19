from decimal import Decimal

from django import template

register = template.Library()

def _price_attr(price, attr):
    if price is None:
        return Decimal('0')
    attr = getattr(price, attr)
    if attr is None:
        return Decimal('0')
    return attr

@register.filter
def gross(price):
    return _price_attr(price, 'gross')

@register.filter
def tax(price):
    return _price_attr(price, 'tax')

@register.filter
def shipping(price):
    return _price_attr(price, 'shipping')

@register.filter
def handling(price):
    return _price_attr(price, 'handling')

@register.filter
def shipping_handling(price):
    return _price_attr(price, 'shipping_handling')

@register.filter
def other(price):
    return _price_attr(price, 'other')

@register.filter
def net(price):
    return _price_attr(price, 'net')

