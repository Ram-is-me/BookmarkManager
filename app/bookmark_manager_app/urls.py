from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('dummydata', views.dummydata, name='dummydata'),
    path('<str:name>/', views.groups, name='groups'),
    path('<str:name>/groups/<str:group>', views.bookmarks, name='bookmarks'),
    path('<str:name>/tags/<str:tag>', views.bookmarks_tag, name='bookmarks_tag'),
    path('<str:name>/bookmark/<int:id>', views.view_bookmark, name='view_bookmark'),
    path('<str:name>/bookmark/<int:id>/removetag/<int:tagid>', views.remove_tag_from_bookmark, name='remove_tag'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
]