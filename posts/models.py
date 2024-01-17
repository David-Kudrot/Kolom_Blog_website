from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAccountModel
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name



 
    
class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="posts/photos")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_name")
    author = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE, related_name="author")
    category = models.ManyToManyField(Category)
    save_post = models.BooleanField(default=False, null=True, blank=True)

    
    def __str__(self) -> str:
        return self.title
    
#for saving post    
class Library(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_posts = models.ManyToManyField(Post, related_name='saved_posts')
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def saved_post_titles(self):
        return self.saved_posts.values_list('title', flat=True)
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.text[:50]}"