from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from .. import models
from .forms import TagForm, GroupForm, SearchForm, FilterForm
import logging

logger = logging.getLogger(__name__)

@login_required
def search_bookmarks(request, name):
    logger.info("Retrieving user with name={}".format(name))
    curr_user = models.User.objects.get(name=name)
    search_val = request.POST.get('search_val')
    search_form = SearchForm()
    search_form.fields['search_val'].initial = search_val

    # Getting required variables from DB
    logger.info("Retrieving tag of user with username={}".format(name))
    tag_list = models.Tag.objects.filter(creator=curr_user)
    logger.info("Retrieving groups of user with username={}".format(name))
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
    logger.info("Retrieving bookmarks of user with username={}".format(name))
    all_bookmarks = models.Bookmark.objects.filter(creator=curr_user)
    bookmark_list_by_keyword = []
    if search_val:
        logger.info("Filtering bookmarks by search value={}".format(search_val))
        bookmark_list_by_keyword_name = all_bookmarks.filter(custom_name__icontains = search_val)
        bookmark_list_by_keyword_note = all_bookmarks.filter(custom_note__icontains = search_val)
        bookmark_list_by_keyword_url = all_bookmarks.filter(url__icontains = search_val)
        logger.info("Merging Bookmarks list based on name and description={}".format(search_val))
        bookmark_list_by_keyword = list(set(bookmark_list_by_keyword_name)| set(bookmark_list_by_keyword_note))
        bookmark_list_by_keyword = list(set(bookmark_list_by_keyword)| set(bookmark_list_by_keyword_url))
    else:
        # logger.debug("Redirecting to Groups page")
        # return HttpResponseRedirect(reverse('groups', args=(name, )))
        bookmark_list_by_keyword = all_bookmarks

    # Getting Tags and Groups from the form
    input_tags = []
    input_groups = []
    tags_check = False
    for key in request.POST:
        if key in all_tag_names:
            if request.POST[key]:
                logger.info("Retrieving tag with id={}".format(key))
                input_tags.append(models.Tag.objects.get(name=key, creator=curr_user))
                filter_form.fields[key].initial = True
        if key in all_group_names:
            if request.POST[key]:
                logger.info("Retrieving group with id={}".format(key))
                input_groups.append(models.Group.objects.get(name=key, creator=curr_user))
                filter_form.fields[key].initial = True
        if key == 'tags_or_check':
            if request.POST[key]:
                logger.info("Checking Tags search option={}".format(key))
                tags_check = True
                # print(filter_form.fields[key])
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
    if tags_check == False:
        for bookmark in bookmark_list_by_group:
            present = 1
            for tag in input_tags:
                if tag not in bookmark.list_of_tags.all():
                    present = 0
                    break
            if present:
                bookmark_list_by_tag.append(bookmark)
    else:
        for bookmark in bookmark_list_by_group:
            present = 0
            for tag in input_tags:
                if tag in bookmark.list_of_tags.all():
                    present = 1
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
    logger.debug("Rendering Search Results page")
    return render(request, 'search.html', context)

