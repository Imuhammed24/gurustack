import base64

from django import template
from django.contrib.auth import get_user_model

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

