from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy, reverse
# from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from . import models
from django import forms

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

def groups(request, name):
    curr_user = models.User.objects.get(name=name)
    group_list = models.Group.objects.filter(creator=curr_user)
    context = {'group_list' : group_list}
    return render(request, 'groups.html', context)

def bookmarks(request, name, group):
    curr_group = models.Group.objects.get(name=group)
    bookmark_list = models.Bookmark.objects.filter(group=curr_group)
    context = {'bookmark_list' : bookmark_list}
    return render(request, 'bookmarks.html', context)

def bookmarks_tag(request, name, tag):
    all_bookmarks = models.Bookmark.objects.all()
    curr_tag = models.Tag.objects.get(name=tag)
    bookmark_list = []
    for bookmark in all_bookmarks:
        if curr_tag in bookmark.list_of_tags.all():
            bookmark_list.append(bookmark)
    context = {'bookmark_list' : bookmark_list}
    return render(request, 'bookmarks_tag.html', context)

class BookmarkForm(forms.Form):
    url = forms.CharField(max_length=500, required=True)
    custom_name = forms.CharField(max_length=200, required=True)
    # list_of_tags_to_add = forms.MultipleChoiceField(
    #     choices=[(r.name,r.name) for r in models.Tag.objects.all()], 
    #     help_text="Control+Click on tags to select multiple. Selected Tags will be added to Associated Tags",
    #     required=False
    #     )
    custom_note = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, group_id, list_of_tag_ids):
        if(models.Bookmark.objects.filter(url=self.url)):
            current_bookmark = models.Bookmark.objects.filter(url=self.url)
            current_bookmark.update(custom_name=self.custom_name)
            current_bookmark.update(custom_note=self.custom_note)
        else:
            new_bookmark = models.Bookmark(url=self.url, custom_name=self.custom_name, custom_note=self.custom_note, group=group_id)
            

def view_bookmark(request, name, id):
    form = BookmarkForm()
    # form.list_of_tags_to_remove.choices
    # list_of_tags_to_remove.choices = [(r.name,r.name) for r in models.Tag.objects.filter(bookmark__id=id).all()]
    if(request.method==POST):


    context = {
        'form': form,
        'bookmark_obj': models.Bookmark.objects.get(id=id),
        'all_tags' : models.Tag.objects.all(),
    }
    return render(request, 'view_bookmark.html', context)

def remove_tag_from_bookmark(request, name, id, tagid):
    return HttpResponse("Remove Tag Function")


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