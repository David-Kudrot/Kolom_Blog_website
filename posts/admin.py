from django.contrib import admin
from .models import Category, Post, Library
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(Library)