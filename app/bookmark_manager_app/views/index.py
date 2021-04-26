from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic
from .. import models

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