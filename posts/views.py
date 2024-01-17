from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Library, Comment, Category
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest
#for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from accounts
from accounts.models import UserAccountModel
from accounts.forms import ProfilePictureForm



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

    if request.user.is_authenticated:
        # Email sending
        email_subject = "Post Saved Confirmation"
        email_body = render_to_string('post_save_email.html', {'post': post, 'user': request.user})
        user_email = request.user.email
        print(user_email)
        email = EmailMultiAlternatives(email_subject, '', to=[user_email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(request, 'Post saved successfully.')
    else:
        messages.error(request, 'Authentication error. Please log in.')

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




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        user_account = UserAccountModel.objects.get(user=user)
        profile_picture_form = ProfilePictureForm(instance=user_account)
        return render(request, 'profile.html', {'user': user, 'user_account': user_account, 'profile_picture_form': profile_picture_form})

    def post(self, request):
        user = request.user
        user_account = UserAccountModel.objects.get(user=user)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_account)

        if profile_picture_form.is_valid():
            profile_picture_form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('profile')

        return render(request, 'profile.html', {'user': user, 'user_account': user_account, 'profile_picture_form': profile_picture_form})
    
    
    
    
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
                 
            print(form.cleaned_data)
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})





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