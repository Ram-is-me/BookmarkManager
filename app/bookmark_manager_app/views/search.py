from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from .. import models
from .forms import TagForm, GroupForm, SearchForm, FilterForm

@login_required
def search_bookmarks(request, name):
    curr_user = models.User.objects.get(name=name)
    search_val = request.POST.get('search_val')
    search_form = SearchForm()
    search_form.fields['search_val'].initial = search_val

    # Getting required variables from DB
    tag_list = models.Tag.objects.filter(creator=curr_user)
    group_list = models.Group.objects.filter(creator=curr_user)
    filter_form = FilterForm(tags=tag_list, groups=group_list)
    filter_form.fields['search_val'].initial = search_val
    
    # tag_form = TagForm(tags=tag_list)
    # tag_form.fields['search_val'].initial = search_val
    # group_form = GroupForm(groups=group_list)
    # group_form.fields['search_val'].initial = search_val

    all_tag_names = [tag.name for tag in tag_list]
    all_group_names = [group.name for group in group_list]
    
    # Searching based on keyword
    all_bookmarks = models.Bookmark.objects.filter(creator=curr_user)
    if search_val:
        bookmark_list_by_keyword = all_bookmarks.filter(custom_name__contains=search_val)
    else:
        return HttpResponseRedirect(reverse('groups', args=(name, )))

    # Getting Tags and Groups from the form
    input_tags = []
    input_groups = []
    for key in request.POST:
        if key in all_tag_names:
            if request.POST[key]:
                input_tags.append(models.Tag.objects.get(name=key))
                filter_form.fields[key].initial = True
        if key in all_group_names:
            if request.POST[key]:
                input_groups.append(models.Group.objects.get(name=key))
                filter_form.fields[key].initial = True
    
    # Searching based on group
    bookmark_list_by_group = []
    # Enabling all groups if none selected
    if(input_groups == []):
        bookmark_list_by_group = bookmark_list_by_keyword
    else:
        for bookmark in bookmark_list_by_keyword:
            present = 0
            for group in input_groups:
                if group.id is bookmark.group.id:
                    present = 1
                    break
            if present:
                bookmark_list_by_group.append(bookmark)


    # Filtering Bookmarks by Tag
    bookmark_list_by_tag = []
    for bookmark in bookmark_list_by_group:
        present = 1
        for tag in input_tags:
            if tag not in bookmark.list_of_tags.all():
                present = 0
                break
        if present:
            bookmark_list_by_tag.append(bookmark)

    

    context= {
        # 'tag_form': tag_form,
        # 'group_form': group_form,
        'filter_form': filter_form,
        'search_form': search_form,
        'bookmark_list': bookmark_list_by_tag,
    }
    return render(request, 'search.html', context)

