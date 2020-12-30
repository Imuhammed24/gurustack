from chat.models import MessageProperty
from posts.forms import CommentForm, ImageForm, TagForm


# @login_required
def check_unread_mssg(request):
    new_message = False
    # check for unread messages
    recipients = []
    total_messages = []
    if request.user.is_authenticated:
        message_receipts = MessageProperty.objects.filter(receiver=request.user)
        for received_message in message_receipts:
            if not received_message.delivered:
                new_message = True
                total_messages.append(received_message)
                if received_message.sender not in recipients:
                    recipients.append(received_message.sender)

        return {
            'unread_message': new_message,
            'new_chat_count': recipients.__len__(),
            'total_messages': total_messages.__len__(),
        }
    else:
        return {
            'no_response': True,
        }


# @login_required
def comment_form_context(request):
    comment_form = CommentForm()
    return {'comment_form': comment_form}


# @login_required
def add_post_context(request):
    image_form = ImageForm()
    return {
        'tag_form': TagForm,
        'image_form': image_form,
    }
