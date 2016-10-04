from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if request.path == pattern:
        return 'active'
    return ''
