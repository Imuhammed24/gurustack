# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Message, Conversation, MessageProperty

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        author_name = data['from']
        recipient_name = data['to']

        author = User.objects.get(username=author_name)
        recipient = User.objects.get(username=recipient_name)

        messages = reversed(Message.objects.filter(author__in=[author, recipient], recipient__in=[author, recipient]))
        # messages_properties = reversed(MessageProperty.objects.filter(message__in=messages))

        content = {
            'command': 'messages',
            # 'message_property': self.messages_properties_to_json(messages_properties),
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author_name = data['from']
        recipient_name = data['to']
        author = get_object_or_404(User, username=author_name)
        recipient = get_object_or_404(User, username=recipient_name)
        if data['message'] is not None and author != recipient:
            message = Message.objects.create(author=author, content=data['message'], recipient=recipient)
            MessageProperty.objects.create(message=message, sender=author, receiver=recipient)

            if Conversation.objects.filter(user1__in=[author, recipient], user2__in=[author, recipient]):
                conversation = Conversation.objects.get(user1__in=[author, recipient], user2__in=[author, recipient])
                conversation.last_message = data['message']
                conversation.save()
            else:
                Conversation.objects.create(user1=author, user2=recipient, last_message=data['message'])

            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
            return self.send_chat_message(content)

    def messages_properties_to_json(self, messages_properties):
        # create json version of the messages from db
        result = []
        for message_property in messages_properties:
            result.append(self.message_property_to_json(message_property))
        return result

    def message_property_to_json(self, message_property):
        return {
            'message': message_property.message.__str__(),
            'sender': message_property.sender.username,
            'receiver': message_property.receiver.username,
            'delivered': str(message_property.delivered)
        }

    def messages_to_json(self, messages):
        # create json version of the messages from db
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'recipient': message.recipient.username,
            'content': message.content,
            'timestamp': str(message.timestamp)[:16]
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        # message = data['message']

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
