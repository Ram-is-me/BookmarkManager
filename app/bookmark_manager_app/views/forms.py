from django import forms
from datetime import date
from .. import models
from django.forms import DateTimeInput

class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context

class BookmarkForm(forms.Form):
    bookmark_id = forms.IntegerField(widget=forms.HiddenInput())
    url = forms.CharField(max_length=500, required=True)
    custom_name = forms.CharField(max_length=50, required=True)
    # list_of_tags_to_add = forms.MultipleChoiceField(
    #     choices=[(r.name,r.name) for r in models.Tag.objects.all()], 
    #     help_text="Control+Click on tags to select multiple. Selected Tags will be added to Associated Tags",
    #     required=False
    #     )
    custom_note = forms.CharField(max_length=200, widget=forms.Textarea, required=False )

    def save(self, url, name, note, bookmark_id):
        current_bookmark = models.Bookmark.objects.filter(id=bookmark_id)
        current_bookmark.update(url = url)
        current_bookmark.update(custom_name = name)
        current_bookmark.update(custom_note = note)    
        current_bookmark.get().save()
        return True

    def new_save(self, request, username, group_id):
        # print(request.POST['custom_name'])
        url_given = request.POST['url']
        if url_given.find('https://')==-1 and url_given.find('http://')==-1 :
            url_given = "https://" + url_given
        new_bookmark = models.Bookmark(
            url=url_given, 
            custom_name=request.POST['custom_name'], 
            custom_note=request.POST['custom_note'], 
            group=models.Group.objects.get(id=group_id), 
            date_of_creation=date.today(), 
            creator=models.User.objects.get(name=username))
        new_bookmark.save()

class FilterForm(forms.Form):
    search_val = forms.CharField(max_length=200)
    tags_or_check = forms.BooleanField(label = 'tags_or_check', required=False)
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tags')
        groups = kwargs.pop('groups')
        super(FilterForm, self).__init__(*args, **kwargs)
        for tag in tags:
            self.fields[tag.name] = forms.BooleanField(label=tag.name, required=False)
        for group in groups:
            self.fields[group.name] = forms.BooleanField(label=group.name, required=False)

class TagForm(forms.Form):
    search_val = forms.CharField(max_length=50, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tags')
        super(TagForm, self).__init__(*args, **kwargs)
        for tag in tags:
            self.fields[tag.name] = forms.BooleanField(label=tag.name)

class GroupForm(forms.Form):
    search_val = forms.CharField(max_length=50, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups')
        super(GroupForm, self).__init__(*args, **kwargs)
        for group in groups:
            self.fields[group.name] = forms.BooleanField(label=group.name)

class SearchForm(forms.Form):
    search_val = forms.CharField(max_length=50)

class ReminderForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label="Name:")
    description = forms.CharField(max_length=200, label="Description")
    # reminder_time = forms.DateTimeField(widget=forms.DateTimeInput(), required=True, help_text="YYYY-MM-DD HH:MM")
    reminder_time = forms.DateTimeField( input_formats=['%d/%m/%Y %H:%M'], widget=BootstrapDateTimePickerInput() )