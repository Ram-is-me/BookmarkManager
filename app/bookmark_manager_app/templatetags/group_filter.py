from django import template
from .. import models

register = template.Library()

@register.filter
def iterate(all_bookmarks, groupid):
    temp = []
    for bookmark in all_bookmarks:
        if bookmark.group.id == groupid:
            temp.append(bookmark)
    return temp
