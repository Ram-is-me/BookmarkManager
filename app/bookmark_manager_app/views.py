from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from . import models
from django import forms
from datetime import date

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def home(request):
    if request.user.is_authenticated:
        if not models.User.objects.filter(name=request.user.username):
            temp = models.User(name=request.user.username)
            temp.save()
        return HttpResponseRedirect(reverse('groups', args=(request.user.username,)))
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def groups(request, name):
    curr_user = models.User.objects.get(name=name)
    group_list = models.Group.objects.filter(creator=curr_user)
    reminder_list = models.Reminder.objects.filter(creator=curr_user)
    tag_list = models.Tag.objects.filter(creator=curr_user)
    all_bookmarks = models.Bookmark.objects.filter(creator=curr_user)
    context = {'group_list' : group_list, 'reminder_list' : reminder_list, 'tag_list' : tag_list, 'all_bookmarks' : all_bookmarks}
    return render(request, 'groups.html', context)

@login_required
def bookmarks(request, name, group):
    curr_user = models.User.objects.get(name=name)
    curr_group = models.Group.objects.get(name=group)
    bookmark_list = models.Bookmark.objects.filter(group=curr_group)
    reminder_list = models.Reminder.objects.filter(creator=curr_user)
    tag_list = models.Tag.objects.filter(creator=curr_user)
    context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'tag_list' : tag_list}
    return render(request, 'bookmarks.html', context)

@login_required
def bookmarks_tag(request, name, tag):
    curr_user = models.User.objects.get(name=name)
    all_bookmarks = models.Bookmark.objects.all()
    curr_tag = models.Tag.objects.get(name=tag)
    bookmark_list = []
    for bookmark in all_bookmarks:
        if curr_tag in bookmark.list_of_tags.all():
            bookmark_list.append(bookmark)
    reminder_list = models.Reminder.objects.filter(creator=curr_user)
    tag_list = models.Tag.objects.filter(creator=curr_user)
    context = {'bookmark_list' : bookmark_list, 'reminder_list' : reminder_list, 'tag_list' : tag_list, 'tag' : tag}
    return render(request, 'bookmarks_tag.html', context)

class BookmarkForm(forms.Form):
    url = forms.CharField(max_length=500, required=True, help_text="change url")
    custom_name = forms.CharField(max_length=50, required=True, help_text="change name")
    # list_of_tags_to_add = forms.MultipleChoiceField(
    #     choices=[(r.name,r.name) for r in models.Tag.objects.all()], 
    #     help_text="Control+Click on tags to select multiple. Selected Tags will be added to Associated Tags",
    #     required=False
    #     )
    custom_note = forms.CharField(max_length=200, widget=forms.Textarea, required=False )

    def save(self, request, username, group_id):
        if(models.Bookmark.objects.filter(url=request.POST['url'])):
            current_bookmark = models.Bookmark.objects.filter(url=request.POST['url'])
            current_bookmark.update(custom_name=request.POST['custom_name'])
            current_bookmark.update(custom_note=request.POST['custom_note'])
        else:
            print(request.POST['custom_name'])
            new_bookmark = models.Bookmark(
                url=request.POST['url'], 
                custom_name=request.POST['custom_name'], 
                custom_note=request.POST['custom_note'], 
                group=models.Group.objects.get(id=group_id), 
                date_of_creation=date.today(), 
                creator=models.User.objects.get(name=username))
            new_bookmark.save()

def add_bookmark(request, name, group_id):
    # return HttpResponse("Adding new bookmark")
    form = BookmarkForm()

    # if(request.method=="POST"):
    #     if (request.POST['url']==''):
    #         print("Empty URL not allowed")

    context = {
        'form': form,
        'message': message,
        'bookmark_obj': models.Bookmark.objects.get(id=id),
        'all_tags' : models.Tag.objects.all(),
        'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get() ),
        'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=id).group.id)
    }
    return render(request, 'view_bookmark.html', context)


def delete_bookmark(request, name, bookmark_id):
    models.Bookmark.objects.filter(id=bookmark_id).delete()
    return HttpResponseRedirect(reverse('home'),request)


def view_bookmark(request, name, id):
    form = BookmarkForm()
    form.fields['url'].initial = models.Bookmark.objects.get(id=id).url
    form.fields['custom_name'].initial = models.Bookmark.objects.get(id=id).custom_name
    form.fields['custom_note'].initial = models.Bookmark.objects.get(id=id).custom_note
    message = ""
    # form.list_of_tags_to_remove.choices
    # list_of_tags_to_remove.choices = [(r.name,r.name) for r in models.Tag.objects.filter(bookmark__id=id).all()]
    if(request.method=="POST"):
        if (request.POST['url']==''):
            message = "Empty URL not allowed"
            # return HttpResponseRedirect(reverse('view_bookmark'),request, context)
        elif (request.POST['custom_name']==''):
            message = "Empty Name not allowed"
        else:
            form.save(request, name, id)
            form = BookmarkForm()
            form.fields['url'].initial = models.Bookmark.objects.get(id=id).url
            form.fields['custom_name'].initial = models.Bookmark.objects.get(id=id).custom_name
            form.fields['custom_note'].initial = models.Bookmark.objects.get(id=id).custom_note

    context = {
        'form': form,
        'message': message,
        'bookmark_obj': models.Bookmark.objects.get(id=id),
        'all_tags' : models.Tag.objects.all(),
        'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get() ),
        'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=id).group.id)
    }
    return render(request, 'view_bookmark.html', context)

def remove_tag_from_bookmark(request, name, id, tagid):
    current_bookmark = models.Bookmark.objects.filter(id=id).get()
    current_tag = models.Tag.objects.filter(id=tagid)
    current_bookmark.list_of_tags.remove(current_tag.get().id)
    # return HttpResponse("Remove Tag Function")
    # return HttpResponseRedirect(reverse('view_bookmark'),args=(name, id, ))
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,id, )))

def add_tag_to_bookmark(request, name, id, tagid):
    current_bookmark = models.Bookmark.objects.filter(id=id).get()
    current_tag = models.Tag.objects.filter(id=tagid)
    current_bookmark.list_of_tags.add(current_tag.get())
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,id, )))    

def change_group_of_bookmark(requst, name, id, groupid):
    current_bookmark = models.Bookmark.objects.filter(id=id)
    current_group = models.Group.objects.filter(id=groupid)
    current_bookmark.update(group=current_group)
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,id, )))    
    # return HttpResponse("Change Group Function")
    
@login_required
def add_group(request, name):
    groupname = request.POST.get('groupname')
    curr_user = models.User.objects.get(name=name)
    new_group = models.Group(name=groupname, creator=curr_user, date_of_creation=timezone.now())
    new_group.save()
    return HttpResponseRedirect(reverse('groups', args=(name,)))

@login_required
def add_tag(request, name):
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
def delete_tag(request, name, tag):
    curr_tag = models.Tag.objects.get(name=tag)
    curr_tag.delete()
    return HttpResponseRedirect(reverse('groups', args=(name,)))


def dummydata(request):
    user1 = models.User(name="user1")
    user1.save()
    user2 = models.User(name="user2")
    user2.save()

    tag11 = models.Tag(name="tag11", creator=user1, date_of_creation=timezone.now())
    tag11.save()
    tag12 = models.Tag(name="tag12", creator=user1, date_of_creation=timezone.now())
    tag12.save()
    tag21 = models.Tag(name="tag21", creator=user2, date_of_creation=timezone.now())
    tag21.save()
    tag22 = models.Tag(name="tag22", creator=user2, date_of_creation=timezone.now())
    tag22.save()

    group11 = models.Group(name="group11", creator=user1, date_of_creation=timezone.now())
    group11.save()
    group12 = models.Group(name="group12", creator=user1, date_of_creation=timezone.now())
    group12.save()
    group21 = models.Group(name="group21", creator=user2, date_of_creation=timezone.now())
    group21.save()
    group22 = models.Group(name="group22", creator=user2, date_of_creation=timezone.now())
    group22.save()

    bkmark11 = models.Bookmark(custom_name="bkmark11", creator=user1, group=group11, date_of_creation=timezone.now())
    bkmark11.save()
    bkmark12 = models.Bookmark(custom_name="bkmark12", creator=user1, group=group11, date_of_creation=timezone.now())
    bkmark12.save()
    bkmark13 = models.Bookmark(custom_name="bkmark13", creator=user1, group=group12, date_of_creation=timezone.now())
    bkmark13.save()
    bkmark14 = models.Bookmark(custom_name="bkmark14", creator=user1, group=group12, date_of_creation=timezone.now())
    bkmark14.save()
    bkmark21 = models.Bookmark(custom_name="bkmark21", creator=user2, group=group21, date_of_creation=timezone.now())
    bkmark21.save()
    bkmark22 = models.Bookmark(custom_name="bkmark22", creator=user2, group=group21, date_of_creation=timezone.now())
    bkmark22.save()
    bkmark23 = models.Bookmark(custom_name="bkmark23", creator=user2, group=group22, date_of_creation=timezone.now())
    bkmark23.save()
    bkmark24 = models.Bookmark(custom_name="bkmark24", creator=user2, group=group22, date_of_creation=timezone.now())
    bkmark24.save()

    bkmark11.list_of_tags.add(tag11)
    bkmark11.save()
    bkmark12.list_of_tags.add(tag11, tag12)
    bkmark12.save()
    bkmark13.list_of_tags.add(tag12)
    bkmark13.save()
    bkmark14.list_of_tags.add(tag11, tag12)
    bkmark14.save()
    bkmark21.list_of_tags.add(tag21)
    bkmark21.save()
    bkmark22.list_of_tags.add(tag21, tag22)
    bkmark22.save()
    bkmark23.list_of_tags.add(tag22)
    bkmark23.save()
    bkmark24.list_of_tags.add(tag21, tag22)
    bkmark24.save()

    reminder1 = models.Reminder(name="reminder1", creator=user1, bookmark=bkmark14, reminder_time=timezone.now()+datetime.timedelta(days=10), time_of_creation=timezone.now())
    reminder1.save()
    reminder2 = models.Reminder(name="reminder2", creator=user2, bookmark=bkmark24, reminder_time=timezone.now()+datetime.timedelta(days=20), time_of_creation=timezone.now())
    reminder2.save()

    return HttpResponse("Dummy Data Initialized")