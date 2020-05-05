import base64

from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from chat.models import Message, MessageProperty

User = get_user_model()
register = template.Library()


def base64_encode(string):
    """
    Removes any `=` used as padding from the encoded string.
    """
    encoded = base64.urlsafe_b64encode(string)
    val = bytes('=', 'utf-8')
    return encoded.rstrip(val)


@register.simple_tag
def encode_url(request_user, target_user):
    request_user = User.objects.get(username=request_user)
    target_user = User.objects.get(username=target_user)

    if request_user.date_joined > target_user.date_joined:
        encode_string = str(request_user.date_joined) + 'secnd' + str(target_user.date_joined)
    else:
        encode_string = str(target_user.date_joined) + 'secnd' + str(request_user.date_joined)

    return str(base64_encode(bytes(encode_string, 'utf-8')))[2:-2]


@register.simple_tag
def get_unread_messages(request_user_username, recipient_username):
    request_user = get_object_or_404(User, username=request_user_username)
    recipient = get_object_or_404(User, username=recipient_username)

    chat = Message.objects.filter(author__in=[request_user, recipient], recipient__in=[request_user, recipient])
    count = 0
    for message in chat:
        if message.recipient == request_user:
            props = MessageProperty.objects.get(message=message)
            if not props.delivered:
                count += 1
    if count == 0:
        return ''
    elif count >= 1:
        return f"{count}"
