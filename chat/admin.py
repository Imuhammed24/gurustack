from django.contrib import admin

from .models import Message, Conversation, MessageProperty


class MessagePropertyInline(admin.TabularInline):
    model = MessageProperty
    raw_id_fields = ['message']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'timestamp', 'recipient']
    list_filter = ['timestamp', 'author', 'recipient']
    inlines = [MessagePropertyInline]


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'last_message']


admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)
