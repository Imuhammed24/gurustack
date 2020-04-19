from django.contrib import admin

from .models import Message, Conversation


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'timestamp', 'recipient']


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'timestamp', 'last_message']


admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)
