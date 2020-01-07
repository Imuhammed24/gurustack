from django.urls import path
from .views import create_post, add_comment

urlpatterns = [
    # path('like/', post_like, name='like'),
    path('create/', create_post, name='create-post'),
    path('add-comment/<pk>', add_comment, name='add-comment')
]
