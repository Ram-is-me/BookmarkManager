from django import template
from .. import models

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

@register.filter
def custom_group_filter(all_objs, group):
    l=[]
    print(group)
    for r in all_objs:
        print(r)    
        if r.id != group.id:
            l.append(r)
    print(l)
    return l