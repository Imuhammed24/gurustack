from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    article = models.CharField(max_length=450)
    tags = TaggableManager(blank=True, verbose_name='Tags')
    image = models.ImageField(upload_to='post-images/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ['created']



#  def get_image_filename(instance):
#     id = instance.post.id
#     return f"post_images/{id}"
# class Images(models.Model):
#     post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to=get_image_filename, verbose_name='Image', blank=True)
