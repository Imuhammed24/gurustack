from django.urls import path

from .views import create_post, add_comment, post_detail_view

urlpatterns = [
    path('detail/<int:i_d>/<str:slug>/', post_detail_view, name='detail'),
    # path('like/', post_like, name='like'),
    path('create/', create_post, name='create-post'),
    path('add-comment/<pk>', add_comment, name='add-comment'),
]
