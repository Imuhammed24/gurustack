from django.urls import path

from account.views import room

urlpatterns = [
    # path('', messages, name='index'),
    path('<str:room_name>/', room, name='room'),
]
