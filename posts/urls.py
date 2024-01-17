from django.urls import path
from .views import PostDetailView, save_post, LibraryView, delete_post, ProfileView, edit_post, create_post

urlpatterns = [
    # path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('save_post/<int:pk>/', save_post, name='save_post'),
    path('library/', LibraryView.as_view(), name='library'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:pk>/', edit_post, name='edit_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
]
