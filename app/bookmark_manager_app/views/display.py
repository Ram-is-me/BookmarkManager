from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.utils import IntegrityError
from .. import models
from .forms import TagForm, SearchForm

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
        lst = models.Reminder.objects.filter(creator=curr_user).order_by('-reminder_time')
        for r in lst:
            r.compute_status()
        output.append(lst)
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
    search_form = SearchForm()
    search_form.fields['search_val'].initial = ""
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
    context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'form' : form, 'search_form': search_form}
    return render(request, 'bookmarks_tag.html', context)

@login_required
def create_group(request, name):
    groupname = request.POST.get('groupname')
    curr_user = models.User.objects.get(name=name)
    try:
        new_group = models.Group(name=groupname, creator=curr_user, date_of_creation=timezone.now())
        new_group.save()
    except IntegrityError:
        return HttpResponseForbidden("<h1> Duplicate group name. Please enter a unique name. </h1>")
    else:
        return HttpResponseRedirect(reverse('groups', args=(name,)))

@login_required
def create_tag(request, name):
    tagname = request.POST.get('tagname')
    curr_user = models.User.objects.get(name=name)
    try:
        new_tag = models.Tag(name=tagname, creator=curr_user, date_of_creation=timezone.now())
        new_tag.save()
    except IntegrityError:
        return HttpResponseForbidden("<h1> Duplicate tag name. Please enter a unique name. </h1>")
    else:
        return HttpResponseRedirect(reverse('groups', args=(name,)))

@login_required
def delete_group(request, name, group):
    curr_group = models.Group.objects.get(name=group)
    curr_group.delete()
    return HttpResponseRedirect(reverse('groups', args=(name,)))
    
@login_required
def delete_tag(request, name):
    deletetagname = request.POST.get('deletetagname')
    try:
        curr_tag = models.Tag.objects.get(name=deletetagname)
        curr_tag.delete()
    except models.Tag.DoesNotExist:
        return HttpResponseForbidden("<h1> Tag does not exist. Please enter a valid name. </h1>")
    else:
        return HttpResponseRedirect(reverse('groups', args=(name,)))