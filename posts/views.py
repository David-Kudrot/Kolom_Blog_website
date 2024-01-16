from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Library, Comment
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest

# class PostListView(View):
#     def get(self, request):
#         posts = Post.objects.all()
#         # for post in posts:
#         #     print(post.title)
#         return render(request, 'home.html', {'posts': posts})


# class PostDetailView(View):
#     def get(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         return render(request, 'post_detail.html', {'post': post})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        total_comments = comments.count()
        form = CommentForm()  #CommentForm
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'total_comments': total_comments, 'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        total_comments = comments.count()

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)

        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'total_comments': total_comments, 'form': form})



@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    library = Library.objects.get_or_create(user=request.user)[0]
    library.saved_posts.add(post)
    messages.success(request, 'Post saved successfully.')
    return redirect('post_detail', pk=pk)



@method_decorator(login_required, name='dispatch')
class LibraryView(View):
    def get(self, request):
        library, created = Library.objects.get_or_create(user=request.user)
        saved_posts = library.saved_posts.all()
        return render(request, 'library.html', {'saved_posts': saved_posts})

    def post(self, request):
        post_id = request.POST.get('post_id') 
        if post_id:
            post = Post.objects.get(pk=post_id)
            library, created = Library.objects.get_or_create(user=request.user)
            library.saved_posts.add(post)
            return redirect('library')  
        return HttpResponseBadRequest("Invalid request")


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseForbidden("You don't have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post, 'type': 'Edit Post'})




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        return render(request, 'profile.html', {'user': user})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the logged-in user is the author of the post
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")

    return redirect('post_list')