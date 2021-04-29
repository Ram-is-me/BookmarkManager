from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic
from .. import models
import logging

logger = logging.getLogger(__name__)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def home(request):
    if request.user.is_authenticated:
        logger.info("User with username={} successfully logged in".format(request.user.username))
        if not models.User.objects.filter(name=request.user.username):
            temp = models.User(name=request.user.username)
            temp.save()
            logger.info("Created new bookmark user with username={}".format(temp.name))
        logger.debug("Redirecting to groups page")
        return HttpResponseRedirect(reverse('groups', args=(request.user.username,)))
    else:
        logger.debug("Redirecting to Login page")
        return HttpResponseRedirect(reverse('login'))