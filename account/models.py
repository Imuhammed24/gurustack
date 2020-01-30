from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    profile_photo = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.CharField(max_length=50, blank=True)
    interests = TaggableManager(blank=True, verbose_name='Interests')
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=30, blank=True)
    year_of_entrance = models.DateField(blank=True, null=True)
    year_of_graduation = models.DateField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    staff_status = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    allow_messages = models.BooleanField(default=True)

    def __str__(self):
        return f'profile for user {self.user.username}'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
