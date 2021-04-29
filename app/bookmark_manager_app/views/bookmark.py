from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from .. import models
from .forms import BookmarkForm

def add_bookmark(request, name, group_id):
    # return HttpResponse("Adding new bookmark")
    form = BookmarkForm()
    message = ""
    id = -1
    new_bm_message = "Create New Bookmark"

    if(request.method=="POST"):
        if (request.POST['url']==''):
            message += "Empty URL not allowed <br>"
            # return HttpResponseRedirect(reverse('view_bookmark'),request, context)
        elif (request.POST['custom_name']==''):
            message += "Empty Name not allowed <br>"
        else:
            form.new_save(request, name, group_id)
            id = models.Bookmark.objects.filter(custom_name= request.POST['custom_name']).get().id
            context = {
                'form': form,
                'message': message,
                'bookmark_obj': models.Bookmark.objects.get(id=id),
                'all_tags' : models.Tag.objects.filter(creator= models.User.objects.filter(name=name).get()),
                'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get()),
                'related_bm' : models.Bookmark.objects.filter(group__id=models.Bookmark.objects.get(id=id).group.id)
            }
            return HttpResponseRedirect(reverse('view_bookmark', args=(name,id, )))

        if(id == -1):
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
    return render(request, 'view_new_bookmark.html', context)

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
            result = form.save(request, name, id)
            if(result == False):
                message = "Can't change both name and URL at the same time."
            else:
                form = BookmarkForm()
                form.fields['url'].initial = models.Bookmark.objects.get(id=id).url
                form.fields['custom_name'].initial = models.Bookmark.objects.get(id=id).custom_name
                form.fields['custom_note'].initial = models.Bookmark.objects.get(id=id).custom_note

    context = {
        'form': form,
        'message': message,
        'bookmark_obj': models.Bookmark.objects.get(id=id),
        'all_tags' : models.Tag.objects.filter(creator= models.User.objects.filter(name=name).get()),
        'all_groups' : models.Group.objects.filter(creator= models.User.objects.filter(name=name).get()),
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