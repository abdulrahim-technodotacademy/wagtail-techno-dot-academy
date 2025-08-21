from django import template

register = template.Library()

@register.filter
def split(value, key=','):
    """
    Splits the string by the key and also removes
    leading/trailing whitespace from each item.
    """
    # This one line splits the string and trims each part.
    return [item.strip() for item in value.split(key)]


@register.filter
def replace(value, args):
    """
    Replaces all occurrences of the first argument with the second argument.
    Usage: {{ some_string|replace:"old,new" }}
    """
    if len(args.split(',')) != 2:
        return value

    old, new = args.split(',')
    return value.replace(old, new)