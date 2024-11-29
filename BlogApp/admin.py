from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'postTitle', 'postContent', 'postDate', 'postEditDate']

admin.site.register(Post, PostAdmin)

# Register your models here.
