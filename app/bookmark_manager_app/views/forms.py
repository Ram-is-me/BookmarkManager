from django import forms
from datetime import date
from .. import models

class BookmarkForm(forms.Form):
    url = forms.CharField(max_length=500, required=True)
    custom_name = forms.CharField(max_length=50, required=True)
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
            return True
        elif (models.Bookmark.objects.filter(name=request.POST['custom_name'])):
            current_bookmark = models.Bookmark.objects.filter(url=request.POST['url'])
            current_bookmark.update(custom_name=request.POST['custom_name'])
            current_bookmark.update(custom_note=request.POST['custom_note'])
            return True
        else:
            return False


    def new_save(self, request, username, group_id):
        print(request.POST['custom_name'])
        new_bookmark = models.Bookmark(
            url=request.POST['url'], 
            custom_name=request.POST['custom_name'], 
            custom_note=request.POST['custom_note'], 
            group=models.Group.objects.get(id=group_id), 
            date_of_creation=date.today(), 
            creator=models.User.objects.get(name=username))
        new_bookmark.save()

class FilterForm(forms.Form):
    search_val = forms.CharField(max_length=50, required=True, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tags')
        groups = kwargs.pop('groups')
        super(FilterForm, self).__init__(*args, **kwargs)
        for tag in tags:
            self.fields[tag.name] = forms.BooleanField(label=tag.name)
        for group in groups:
            self.fields[group.name] = forms.BooleanField(label=group.name)

class TagForm(forms.Form):
    search_val = forms.CharField(max_length=50, required=True, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tags')
        super(TagForm, self).__init__(*args, **kwargs)
        for tag in tags:
            self.fields[tag.name] = forms.BooleanField(label=tag.name)

class GroupForm(forms.Form):
    search_val = forms.CharField(max_length=50, required=True,widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups')
        super(GroupForm, self).__init__(*args, **kwargs)
        for group in groups:
            self.fields[group.name] = forms.BooleanField(label=group.name)

class SearchForm(forms.Form):
    search_val = forms.CharField(max_length=50, required=True)