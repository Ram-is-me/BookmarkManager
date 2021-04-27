from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .. import models
from .forms import TagForm
    
@login_required
def groups(request, name):
    curr_user = models.User.objects.get(name=name)
    group_list = models.Group.objects.filter(creator=curr_user)
    reminder_list = models.Reminder.objects.filter(creator=curr_user)
    tag_list = models.Tag.objects.filter(creator=curr_user)
    form = TagForm(tags=tag_list)
    all_bookmarks = models.Bookmark.objects.filter(creator=curr_user)
    context = {'group_list' : group_list, 'reminder_list' : reminder_list, 'all_bookmarks' : all_bookmarks, 'form' : form}
    return render(request, 'groups.html', context)

# @login_required
# def bookmarks_tag(request, name, tag):
#     curr_user = models.User.objects.get(name=name)
#     all_bookmarks = models.Bookmark.objects.all()
#     curr_tag = models.Tag.objects.get(name=tag)
#     bookmark_list = []
#     for bookmark in all_bookmarks:
#         if curr_tag in bookmark.list_of_tags.all():
#             bookmark_list.append(bookmark)
#     reminder_list = models.Reminder.objects.filter(creator=curr_user)
#     tag_list = models.Tag.objects.filter(creator=curr_user)
#     context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'tag_list' : tag_list, 'tag' : tag}
#     return render(request, 'bookmarks_tag.html', context)

@login_required
def bookmarks_tag(request, name):
    curr_user = models.User.objects.get(name=name)
    tag_list = models.Tag.objects.filter(creator=curr_user)
    form = TagForm(tags=tag_list)
    all_tag_names = [tag.name for tag in tag_list]
    input_tags = []
    for key in request.POST:
        if key in all_tag_names:
            if request.POST[key]:
                input_tags.append(models.Tag.objects.get(name=key))
    print(input_tags)
    all_bookmarks = models.Bookmark.objects.filter(creator=curr_user)
    bookmark_list = []
    for bookmark in all_bookmarks:
        present = 1
        for tag in input_tags:
            if tag not in bookmark.list_of_tags.all():
                present = 0
                break
        if present:
            bookmark_list.append(bookmark)
    reminder_list = models.Reminder.objects.filter(creator=curr_user)
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
    curr_user = models.User.objects.get(name=name)
    curr_tag = models.Tag.objects.get(name=deletetagname)
    curr_tag.delete()
    return HttpResponseRedirect(reverse('groups', args=(name,)))


'''
<form
            action="{% url 'delete_tag' user.username tag %}"
            method="post"
            class="post-form"
          >
            {% csrf_token %} {% buttons %}
            <button type="submit" class="btn btn-danger">Delete Tag</button>
            {% endbuttons %}
          </form>
'''