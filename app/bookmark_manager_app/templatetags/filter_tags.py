from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def humanreadable(text):
    return text.replace('_', ' ').capitalize()

@register.filter
def parse_csv(text):
    return [ x.strip() for x in text.split(',')]

@register.filter
def custom_role_filter(all_objs, used_roles):
    l = []
    for r in all_objs:
        if r not in used_roles:
            l.append(r)
    return l