
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Library
from django.contrib.auth.models import User

class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'post_list.html', {'posts': posts})

class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'post_detail.html', {'post': post})

@method_decorator(login_required, name='dispatch')
class LibraryView(View):
    def get(self, request):
        library = Library.objects.get_or_create(user=request.user)[0]
        saved_posts = library.saved_posts.all()
        return render(request, 'library.html', {'saved_posts': saved_posts})

@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    library = Library.objects.get_or_create(user=request.user)[0]
    library.saved_posts.add(post)
    return redirect('post_detail', pk=pk)
