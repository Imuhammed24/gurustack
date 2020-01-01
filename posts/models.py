from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from io import BytesIO
from django.core.files import File
from PIL import Image


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    article = models.CharField(max_length=450)
    slug = models.CharField(max_length=200, blank=True)
    # tags = TaggableManager(blank=True)
    # image = models.ImageField(upload_to='post-images/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article[:10])
            super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.article[:10]

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])


class Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tag')
    tags = TaggableManager(blank=True)


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
        self.thumbnail = make_thumbnail(self.image, size=(485, 485))

        super().save(*args, **kwargs)

