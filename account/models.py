from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

from posts.models import make_thumbnail


# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    YEAR_OF_ENTRANCE = (
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
    )

    YEAR_OF_GRADUATION = (
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, default='Male', choices=GENDER_CHOICES)
    profile_photo = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.CharField(max_length=70, blank=True)
    interests = TaggableManager(verbose_name='Interests')
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=30, blank=True)
    level = models.IntegerField(blank=True, null=True)
    staff_status = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    allow_messages = models.BooleanField(default=True)
    year_of_entrance = models.CharField(max_length=10, default='2020', choices=YEAR_OF_ENTRANCE)
    year_of_graduation = models.CharField(max_length=10, blank=True, null=True, choices=YEAR_OF_GRADUATION)

    def __str__(self):
        return f'profile for user {self.user.username}'

    def save(self, *args, **kwargs):
        if self.profile_photo:
            self.thumbnail = make_thumbnail(self.profile_photo, size=(90, 90))
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
