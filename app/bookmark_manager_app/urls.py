from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('dummydata', views.dummydata, name='dummydata'),
    path('<str:name>/', views.groups, name='groups'),
    path('<str:name>/groups/<str:group>', views.bookmarks, name='bookmarks'),
    path('<str:name>/tags/<str:tag>', views.bookmarks_tag, name='bookmarks_tag'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
]