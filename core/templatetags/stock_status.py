from django import template

register = template.Library()

@register.inclusion_tag('core/components/stock_badge.html')
def stock_badge(product):
    return {'product': product}
