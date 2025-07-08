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

@register.filter
def ability_modifier(score):
    try:
        score = int(score)
        modifier = (score - 10) // 2
        if modifier >= 0:
            return f" +{modifier}"
        return f" {modifier}"
    except (ValueError, TypeError):
        return "N/A"
