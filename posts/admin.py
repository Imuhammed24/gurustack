from django.contrib import admin
from .models import Post, Tag, Images
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'created']
    list_filter = ['created']


class TagAdmin(admin.ModelAdmin):
    list_display = ['post']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Images, ImagesAdmin)
