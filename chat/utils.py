import base64

from django.contrib.auth import get_user_model

User = get_user_model()


def base64_decode(string):
    """
    Adds back in the required padding before decoding.
    """
    string.encode('utf-8')
    padding = 4 - (len(string) % 4)
    string = string + ("=" * padding)
    return base64.urlsafe_b64decode(string)
