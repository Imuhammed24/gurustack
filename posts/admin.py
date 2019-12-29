from django.contrib import admin
from .models import Post, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['slug', 'image', 'created']
    list_filter = ['created']


class TagAdmin(admin.ModelAdmin):
    list_display = ['post']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
