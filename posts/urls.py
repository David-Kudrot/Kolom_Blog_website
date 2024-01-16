from django.urls import path
from .views import PostListView, PostDetailView, save_post, LibraryView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('save_post/<int:pk>/', save_post, name='save_post'),
    path('library/', LibraryView.as_view(), name='library'),
]
