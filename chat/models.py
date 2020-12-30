from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='message_recipient')

    def __str__(self):
        return f'{self.author.username} and {self.recipient.username}'

    class Meta:
        ordering = ['-timestamp']


class MessageProperty(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='properties')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    delivered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Message Properties'


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations', blank=True)
    last_message = models.TextField()
    last_by = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.participants}'

    def is_past_due(self):
        now = datetime.now().date()
        timestamp = self.timestamp
        one_day_ago = now - timedelta(days=1)
        two_day_ago = now - timedelta(days=2)

        if str(one_day_ago) >= str(timestamp)[:10]:
            return 'yesterday'
        elif str(two_day_ago) >= str(timestamp)[:10]:
            return 'two_days'
        else:
            return 'many_days'

    class Meta:
        ordering = ['-timestamp']
