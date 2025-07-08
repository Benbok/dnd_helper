from django import template

register = template.Library()

@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter
def endswith(text, ends):
    if isinstance(text, str):
        return text.endswith(ends)
    return False