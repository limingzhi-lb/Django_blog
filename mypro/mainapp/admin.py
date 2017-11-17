from django.contrib import admin
from .models import Category, Post, Tag, Comment, Me, Message


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Me)
admin.site.register(Message)