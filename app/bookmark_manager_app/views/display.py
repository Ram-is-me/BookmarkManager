from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.utils import IntegrityError
from .. import models
from .forms import TagForm, SearchForm
import logging

logger = logging.getLogger(__name__)

from django.utils import timezone
import datetime

def helper(arr, name):
    output = []
    logger.info("Retrieving user with name={}".format(name))
    curr_user = models.User.objects.get(name=name)
    output.append(curr_user)
    if "g" in arr:
        logger.info("Retrieving groups of user with username={}".format(name))
        output.append(models.Group.objects.filter(creator=curr_user).order_by('name'))
    if "b" in arr:
        logger.info("Retrieving bookmarks of user with username={}".format(name))
        output.append(models.Bookmark.objects.filter(creator=curr_user))
    if "t" in arr:
        logger.info("Retrieving tags of user with username={}".format(name))
        output.append(models.Tag.objects.filter(creator=curr_user))
    if "r" in arr:
        logger.info("Retrieving reminders of user with username={}".format(name))
        lst = models.Reminder.objects.filter(creator=curr_user).order_by('reminder_time')
        logger.info("Updating status of all reminders")
        for r in lst:
            r.compute_status()
        output.append(lst)
    return output

def render_groups(request, name, msg):
    new_grp_msg = ""
    new_tag_msg = ""
    rem_grp_msg = ""
    rem_tag_msg = ""
    dup_grp_msg = ""
    dup_tag_msg = ""
    inv_grp_msg = ""
    inv_tag_msg = ""

    if msg == 'ng':
        new_grp_msg = "Group added successfully."
    if msg == 'nt':
        new_tag_msg = "Tag added successfully."
    if msg == 'rg':
        rem_grp_msg = "Group removed successfully."
    if msg == 'rt':
        rem_tag_msg = "Tag removed successfully."
    if msg == 'dg':
        dup_grp_msg = "Duplicate group name. Please enter a unique name."
    if msg == 'dt':
        dup_tag_msg = "Duplicate tag name. Please enter a unique name."
    if msg == 'ig':
        inv_grp_msg = "Group does not exist. Please enter a valid name."
    if msg == 'it':
        inv_tag_msg = "Tag does not exist. Please enter a valid name."

    curr_user, group_list, all_bookmarks, tag_list, reminder_list = helper(["g", "b", "t", "r"], name)
    form = TagForm(tags=tag_list)
    context = {'group_list' : group_list, 'reminder_list' : reminder_list, 'all_bookmarks' : all_bookmarks, 'form' : form,
        'new_grp_msg' : new_grp_msg,
        'new_tag_msg' : new_tag_msg,
        'rem_grp_msg' : rem_grp_msg,
        'rem_tag_msg' : rem_tag_msg,
        'dup_grp_msg' : dup_grp_msg,
        'dup_tag_msg' : dup_tag_msg,
        'inv_grp_msg' : inv_grp_msg,
        'inv_tag_msg' : inv_tag_msg,
    }
    logger.debug("Rendering Groups page")
    return render(request, 'groups.html', context)
    
@login_required
def groups(request, name):
    logger.debug("Redirected to groups page")
    return render_groups(request, name, '')

@login_required
def bookmarks_tag(request, name):
    logger.debug("Redirected to tag filter page")
    curr_user, all_bookmarks, tag_list, reminder_list = helper(["b", "t", "r"], name)
    form = TagForm(tags=tag_list)
    search_form = SearchForm()
    search_form.fields['search_val'].initial = ""
    all_tag_names = [tag.name for tag in tag_list]
    input_tags = []
    for key in request.POST:
        if key in all_tag_names and request.POST[key]:
                logger.info("Retrieving tag with name={}".format(key))
                input_tags.append(models.Tag.objects.get(name=key))
    bookmark_list = []
    all_bookmarks = all_bookmarks.order_by('-date_of_creation')
    for bookmark in all_bookmarks:
        present = 1
        for tag in input_tags:
            if tag not in bookmark.list_of_tags.all():
                present = 0
                break
        if present:
            bookmark_list.append(bookmark)
    context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'form' : form, 'search_form': search_form, 'input_tags' : input_tags}
    logger.debug("Rendering Tag Filter page")
    return render(request, 'bookmarks_tag.html', context)

@login_required
def create_group(request, name):
    logger.debug("Trying to create new group")
    groupname = request.POST.get('groupname')
    logger.info("Retrieving user with name={}".format(name))
    curr_user = models.User.objects.get(name=name)
    try:
        new_group = models.Group(name=groupname, creator=curr_user, date_of_creation=timezone.now())
        new_group.save()
        logger.info("Created new group with name={}".format(groupname))
    except IntegrityError:
        logger.error("Duplicate group name {}".format(groupname))
        return render_groups(request, name, 'dg')
    else:
        return render_groups(request, name, 'ng')

@login_required
def create_tag(request, name):
    logger.debug("Trying to create new tag")
    tagname = request.POST.get('tagname')
    logger.info("Retrieving user with name={}".format(name))
    curr_user = models.User.objects.get(name=name)
    try:
        new_tag = models.Tag(name=tagname, creator=curr_user, date_of_creation=timezone.now())
        new_tag.save()
        logger.info("Created new tag with name={}".format(tagname))
    except IntegrityError:
        logger.error("Duplicate tag name {}".format(tagname))
        return render_groups(request, name, 'dt')
    else:
        return render_groups(request, name, 'nt')

@login_required
def delete_group(request, name):
    logger.debug("Trying to delete existing group")
    deletegroupname = request.POST.get('deletegroupname')
    try:
        logger.info("Retrieving group with name={}".format(deletegroupname))
        curr_group = models.Group.objects.get(name=deletegroupname)
        curr_group.delete()
        logger.info("Deleted group with name={}".format(deletegroupname))
    except models.Group.DoesNotExist:
        logger.error("Invalid group name {}".format(deletegroupname))
        return render_groups(request, name, 'ig')
    else:
        return render_groups(request, name, 'rg')
    
@login_required
def delete_tag(request, name):
    logger.debug("Trying to delete existing tag")
    deletetagname = request.POST.get('deletetagname')
    try:
        logger.info("Retrieving tag with name={}".format(deletetagname))
        curr_tag = models.Tag.objects.get(name=deletetagname)
        curr_tag.delete()
        logger.info("Deleted tag with name={}".format(deletetagname))
    except models.Tag.DoesNotExist:
        logger.error("Invalid tag name {}".format(deletetagname))
        return render_groups(request, name, 'it')
    else:
        return render_groups(request, name, 'rt')

@login_required
def delete_reminder(request, name, reminder):
    logger.debug("Trying to delete reminder")
    logger.info("Retrieving reminder with name={}".format(reminder))
    curr_reminder = models.Reminder.objects.get(name=reminder)
    curr_reminder.delete()
    logger.info("Deleted reminder with name={}".format(reminder))
    return HttpResponseRedirect(reverse('groups', args=(name, )), request)