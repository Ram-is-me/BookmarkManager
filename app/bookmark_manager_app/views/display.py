from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .. import models
from .forms import TagForm

def helper(arr, name):
    output = []
    curr_user = models.User.objects.get(name=name)
    output.append(curr_user)
    if "g" in arr:
        output.append(models.Group.objects.filter(creator=curr_user))
    if "b" in arr:
        output.append(models.Bookmark.objects.filter(creator=curr_user))
    if "t" in arr:
        output.append(models.Tag.objects.filter(creator=curr_user))
    if "r" in arr:
        output.append(models.Reminder.objects.filter(creator=curr_user))
    return output
    
@login_required
def groups(request, name):
    curr_user, group_list, all_bookmarks, tag_list, reminder_list = helper(["g", "b", "t", "r"], name)
    form = TagForm(tags=tag_list)
    context = {'group_list' : group_list, 'reminder_list' : reminder_list, 'all_bookmarks' : all_bookmarks, 'form' : form}
    return render(request, 'groups.html', context)

@login_required
def bookmarks_tag(request, name):
    curr_user, all_bookmarks, tag_list, reminder_list = helper(["b", "t", "r"], name)
    form = TagForm(tags=tag_list)
    all_tag_names = [tag.name for tag in tag_list]
    input_tags = []
    for key in request.POST:
        if key in all_tag_names and request.POST[key]:
                input_tags.append(models.Tag.objects.get(name=key))
    bookmark_list = []
    for bookmark in all_bookmarks:
        present = 1
        for tag in input_tags:
            if tag not in bookmark.list_of_tags.all():
                present = 0
                break
        if present:
            bookmark_list.append(bookmark)
    context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'form' : form}
    return render(request, 'bookmarks_tag.html', context)

@login_required
def create_group(request, name):
    groupname = request.POST.get('groupname')
    curr_user = models.User.objects.get(name=name)
    new_group = models.Group(name=groupname, creator=curr_user, date_of_creation=timezone.now())
    new_group.save()
    return HttpResponseRedirect(reverse('groups', args=(name,)))

@login_required
def create_tag(request, name):
    tagname = request.POST.get('tagname')
    curr_user = models.User.objects.get(name=name)
    new_tag = models.Tag(name=tagname, creator=curr_user, date_of_creation=timezone.now())
    new_tag.save()
    return HttpResponseRedirect(reverse('groups', args=(name,)))

@login_required
def delete_group(request, name, group):
    curr_group = models.Group.objects.get(name=group)
    curr_group.delete()
    return HttpResponseRedirect(reverse('groups', args=(name,)))
    
@login_required
def delete_tag(request, name):
    deletetagname = request.POST.get('deletetagname')
    curr_tag = models.Tag.objects.get(name=deletetagname)
    curr_tag.delete()
    return HttpResponseRedirect(reverse('groups', args=(name,)))