from datetime import datetime, timedelta

import pytz
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.


class Message (models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='message_recipient')

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-timestamp']


class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_with')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_from')
    last_message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user1.username} and {self.user2.username}'

    def is_past_due(self):
        now = datetime.now()
        now = pytz.utc.localize(now)
        one_day_ago = now - timedelta(days=1)
        two_day_ago = now - timedelta(days=2)
        if self.timestamp > one_day_ago:
            return 'yesterday'
        elif two_day_ago >= self.timestamp:
            return 'two_days'

    class Meta:
        ordering = ['-timestamp']
