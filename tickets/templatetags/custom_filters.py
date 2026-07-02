from django import template

register = template.Library()


@register.filter
def model_type(instance):
    return instance.__class__.__name__
