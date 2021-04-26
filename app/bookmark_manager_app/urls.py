from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('dummydata', views.dummydata, name='dummydata'),
    path('<str:name>/', views.groups, name='groups'),
    path('<str:name>/groups/<str:group>', views.bookmarks, name='bookmarks'),
    path('<str:name>/tags/<str:tag>', views.bookmarks_tag, name='bookmarks_tag'),
    path('<str:name>/<int:group_id>/bookmark/new/', views.add_bookmark, name='add_bookmark'),
    path('<str:name>/bookmark/<int:bookmark_id>/delete', views.delete_bookmark, name='delete_bookmark'),
    path('<str:name>/bookmark/<int:id>', views.view_bookmark, name='view_bookmark'),
    path('<str:name>/bookmark/<int:id>/removetag/<int:tagid>', views.remove_tag_from_bookmark, name='remove_tag'),
    path('<str:name>/bookmark/<int:id>/addtag/<int:tagid>', views.add_tag_to_bookmark, name='add_tag'),
    path('<str:name>/bookmark/<int:id>/changegroup/<int:groupid>', views.change_group_of_bookmark, name='change_group'),
    path('<str:name>/addgroup', views.add_group, name='add_group'),
    path('<str:name>/addtag', views.add_tag, name='add_tag'),
    path('<str:name>/deletegroup/<str:group>', views.delete_group, name='delete_group'),
    path('<str:name>/deletetag/<str:tag>', views.delete_tag, name='delete_tag'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
]