from io import BytesIO

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    article = models.CharField(max_length=450)
    slug = models.CharField(max_length=200, blank=True)
    # tags = TaggableManager(blank=True)
    # image = models.ImageField(upload_to='post-images/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_likes',
                                        blank=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article[:10])
            super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.article[:10]

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.content[:10]


class Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tag')
    tags = TaggableManager(blank=True, help_text=None, verbose_name='')


def get_image_filename(instance, filename):
    slug = instance.post.slug
    return f"post_images/{slug}-{filename}"


def make_thumbnail(image, size=(100, 100)):
    """Makes thumbnails of given size from given image"""
    im = Image.open(image)
    im.convert('RGB')  # convert mode
    im.thumbnail(size)  # resize image
    thumb_io = BytesIO()  # create a BytesIO object
    im.save(thumb_io, 'JPEG', quality=85)  # save image to BytesIO object
    thumbnail = File(thumb_io, name=image.name)  # create a django friendly File object
    return thumbnail


class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Images'

    def save(self, *args, **kwargs):
        self.thumbnail = make_thumbnail(self.image, size=(70, 70))

        super().save(*args, **kwargs)

