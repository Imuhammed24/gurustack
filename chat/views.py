from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

#
# def index(request):
#     users = User.objects.all()
#
#     context = {
#         'users': users,
#     }
#
#     return render(request, 'chat/index.html', context)
#
#
# @login_required
# def room(request, room_name):
#     room_name_4_decode = base64_decode(room_name)
#     extracted_timezones = room_name_4_decode.decode("utf-8")
#     split_timezones = extracted_timezones.split('secnd')
#     target_date = None
#     request_legitimacy = False
#
#     for date in split_timezones:
#         parsed_date = parse(date)
#         if request.user.date_joined != parsed_date:
#             target_date = parsed_date
#         else:
#             request_legitimacy = True
#     if request_legitimacy is True:
#         user = get_object_or_404(User, date_joined=target_date)
#         context = {
#             'user': user,
#             'room_name': room_name
#         }
#         return render(request, 'chat/room.html', context)
#     else:
#         return redirect('chat:index')
