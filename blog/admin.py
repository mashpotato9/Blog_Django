from django.contrib import admin
from .models import Category, Blog, Comment

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'content')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'created_at', 'content')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
    