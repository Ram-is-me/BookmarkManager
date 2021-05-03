from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date,datetime
from .. import models
from .forms import BookmarkForm, ReminderForm
import logging

logger = logging.getLogger(__name__)
reminder_message = ""

def add_bookmark(request, name, group_id):
    logger.debug("Redirected to Add Bookmark page")
    form = BookmarkForm()
    message = ""
    bookmark_id = -1
    new_bm_message = "Create New Bookmark"

    if(request.method=="POST"):
        if (request.POST['url']==''):
            message += "Empty URL not allowed <br>"
            # return HttpResponseRedirect(reverse('view_bookmark'),request, context)
        elif (request.POST['custom_name']==''):
            message += "Empty Name not allowed <br>"
        else:
            form.new_save(request, name, group_id)
            logger.info("Retrieving bookmark with custom name={}".format(request.POST['custom_name']))
            bookmark_id = models.Bookmark.objects.filter(custom_name= request.POST['custom_name']).get().id
            context = {
                'form': form,
                'message': message,
                'bookmark_obj': models.Bookmark.objects.get(id=bookmark_id),
                'all_tags' : models.Tag.objects.filter(creator= models.User.objects.filter(name=name).get()),
                'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get()),
                'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=bookmark_id).group.id)
            }
            logger.debug("Redirecting to View Bookmark page")
            return HttpResponseRedirect(reverse('view_bookmark', args=(name,bookmark_id, )))

        if(bookmark_id == -1):
            message = "Insertion Failed"
    
    context = {
        'form': form,
        'new_bm_message': new_bm_message,
        'message': message,
        # 'bookmark_obj': models.Bookmark.objects.get(id=new_bookmark_id),
        # 'all_tags' : models.Tag.objects.filter(creator= models.User.objects.filter(name=name).get()),
        # 'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get()),
        # 'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=id).group.id)
    }
    logger.debug("Rendering View New Bookmark page")
    return render(request, 'view_new_bookmark.html', context)

def delete_bookmark(request, name, bookmark_id):
    models.Bookmark.objects.filter(id=bookmark_id).delete()
    logger.info("Deleted bookmark with id={}".format(bookmark_id))
    logger.debug("Redirecting to Groups page")
    return HttpResponseRedirect(reverse('groups', args=(name,)),request)


def view_bookmark(request, name, bookmark_id):
    logger.debug("Redirected to Edit Bookmark page")
    logger.info("Retrieving bookmark with id={}".format(id))
    form = BookmarkForm()
    form.fields['bookmark_id'].initial = bookmark_id
    form.fields['url'].initial = models.Bookmark.objects.get(id=bookmark_id).url
    form.fields['custom_name'].initial = models.Bookmark.objects.get(id=bookmark_id).custom_name
    form.fields['custom_note'].initial = models.Bookmark.objects.get(id=bookmark_id).custom_note
    reminder_form = ReminderForm()
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
            # print(request.POST['custom_name'])
            result = form.save( request.POST['url'], 
            request.POST['custom_name'],
            request.POST['custom_note'],
            bookmark_id
            )
            if(result == False):
                message = "Can't change both name and URL at the same time."
            else:
                logger.info("Retrieving bookmark with id={}".format(bookmark_id))
                form = BookmarkForm()
                form.fields['url'].initial = models.Bookmark.objects.get(id=bookmark_id).url
                form.fields['custom_name'].initial = models.Bookmark.objects.get(id=bookmark_id).custom_name
                form.fields['custom_note'].initial = models.Bookmark.objects.get(id=bookmark_id).custom_note

    logger.info("Updating status of all reminders")
    all_reminders = models.Reminder.objects.filter(bookmark__id=bookmark_id)
    for r in all_reminders:
        r.compute_status()
    
    logger.info("Retrieving bookmark with id={}".format(bookmark_id))
    logger.info("Retrieving user with name={}".format(name))
    logger.info("Retrieving tags of user with username={}".format(name))
    logger.info("Retrieving groups of user with username={}".format(name))
    logger.info("Retrieving bookmarks with group id={}".format(models.Bookmark.objects.get(id=bookmark_id).group.id))
    context = {
        'form': form,
        'reminder_form': reminder_form,
        'message': message,
        'bookmark_obj': models.Bookmark.objects.get(id=bookmark_id),
        'all_tags' : models.Tag.objects.filter(creator= models.User.objects.filter(name=name).get()),
        'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get()),
        'all_reminders' : all_reminders,
        'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=bookmark_id).group.id)
    }
    logger.debug("Rendering View Bookmark page")
    return render(request, 'view_bookmark.html', context)

def remove_tag_from_bookmark(request, name, bookmark_id, tagid):
    logger.info("Retrieving bookmark with id={}".format(bookmark_id))
    current_bookmark = models.Bookmark.objects.filter(id=bookmark_id).get()
    logger.info("Retrieving tag with id={}".format(tagid))
    current_tag = models.Tag.objects.filter(id=tagid)
    logger.info("Removing tag with id={} from list of tags of bookmark with id={}".format(tagid, bookmark_id))
    current_bookmark.list_of_tags.remove(current_tag.get().id)
    logger.debug("Redirecting to View Bookmark page")
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,bookmark_id, )))

def add_tag_to_bookmark(request, name, bookmark_id, tagid):
    logger.info("Retrieving bookmark with id={}".format(bookmark_id))
    current_bookmark = models.Bookmark.objects.filter(id=bookmark_id).get()
    logger.info("Retrieving tag with id={}".format(tagid))
    current_tag = models.Tag.objects.filter(id=tagid)
    logger.info("Adding tag with id={} to list of tags of bookmark with id={}".format(tagid, bookmark_id))
    current_bookmark.list_of_tags.add(current_tag.get())
    logger.debug("Redirecting to View Bookmark page")
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,bookmark_id, )))    

def change_group_of_bookmark(requst, name, bookmark_id, groupid):
    logger.info("Retrieving bookmark with id={}".format(bookmark_id))
    current_bookmark = models.Bookmark.objects.filter(id=bookmark_id)
    logger.info("Retrieving group with id={}".format(groupid))
    current_group = models.Group.objects.filter(id=groupid).get()
    print("LOL"+current_group.name)
    logger.info("Updating group of bookmark with id={} to group with id={}".format(bookmark_id, groupid))
    current_bookmark.update(group=current_group)
    logger.debug("Redirecting to View Bookmark page")
    return HttpResponseRedirect(reverse('view_bookmark', args=(name,bookmark_id, )))    

def add_reminder(request, name, bookmark_id):
    
    form = ReminderForm()
    reminder_name = request.POST['name']
    reminder_description = request.POST['description']
    reminder_time = request.POST['reminder_time']
    if(models.Reminder.objects.filter(name = reminder_name)):
        reminder_message = "Give Unique Reminder Name"
        return HttpResponseRedirect(reverse('view_bookmark',args=(name,bookmark_id, )))
    else:
        new_reminder = models.Reminder(
            name = reminder_name, 
            description = reminder_description, 
            reminder_time = reminder_time, 
            time_of_creation = datetime.now(),
            creator= models.User.objects.get(name=name),
            bookmark = models.Bookmark.objects.get(id=bookmark_id)   
            )
        new_reminder.save()
    # return HttpResponse("Reminder Added")
    print("Reminder Added")
    return HttpResponseRedirect(reverse('view_bookmark',args=(name,bookmark_id, )))
