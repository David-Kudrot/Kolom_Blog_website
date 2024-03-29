from django.shortcuts import render
from django.views import View
from posts.models import Post, Category
from django.db.models import Q
from django.views.generic import TemplateView


class Home(View):
    def get(self, request, category_slug=None):
        posts = Post.objects.all()
        categories = Category.objects.all()
        
        return render(request, 'home.html', {'posts': posts, 'categories': categories})
    


class Blogs(View):
    def get(self, request, category_slug=None):
        posts = Post.objects.all()

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            posts = posts.filter(category=category)

        categories = Category.objects.all()
        
        # add search query
        search_query = request.GET.get('q', '')
        category_filter = request.GET.get('category', '')
        author_filter = request.GET.get('author', '')
        date_filter = request.GET.get('date', '')


        # Apply search query
        if search_query:
            posts = posts.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))

        # Apply category filter
        if category_filter:
            posts = posts.filter(category__name=category_filter)

        if date_filter:
            posts = posts.filter(created_at__date=date_filter)

        
        return render(request, 'blogs.html', {'posts': posts, 'categories': categories})
    
    
