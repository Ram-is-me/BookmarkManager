from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.home, name='home'),
    # path('dummydata', views.data, name='dummydata'),
    path('<str:name>/', views.display.groups, name='groups'),
    path('<str:name>/tagfilter', views.display.bookmarks_tag, name='bookmarks_tag'),
    path('<str:name>/<int:group_id>/bookmark/new/', views.bookmark.add_bookmark, name='add_bookmark'),
    path('<str:name>/bookmark/<int:bookmark_id>/delete', views.bookmark.delete_bookmark, name='delete_bookmark'),
    path('<str:name>/bookmark/<int:id>', views.bookmark.view_bookmark, name='view_bookmark'),
    path('<str:name>/bookmark/<int:id>/removetag/<int:tagid>', views.bookmark.remove_tag_from_bookmark, name='remove_tag'),
    path('<str:name>/bookmark/<int:id>/addtag/<int:tagid>', views.bookmark.add_tag_to_bookmark, name='add_tag'),
    path('<str:name>/bookmark/<int:id>/changegroup/<int:groupid>', views.bookmark.change_group_of_bookmark, name='change_group'),
    path('<str:name>/creategroup', views.display.create_group, name='create_group'),
    path('<str:name>/createtag', views.display.create_tag, name='create_tag'),
    path('<str:name>/deletegroup/<str:group>', views.display.delete_group, name='delete_group'),
    path('<str:name>/deletetag', views.display.delete_tag, name='delete_tag'),
    path('<str:name>/search', views.search.search_bookmarks, name='search'),
    path('accounts/signup', views.index.SignUpView.as_view(), name='signup'),
]