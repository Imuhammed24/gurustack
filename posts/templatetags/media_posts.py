# from django import template
# from django.template.loader import get_template
# from ..models import Post
# from django.db.models import Count
#
# register = template.Library()
#
# #
# # @register.inclusion_tag('popular_posts.html')
# # def popular_posts():
# #     all_popular_post = BlogPost.objects.published().annotate(comments_no=Count('comments')).distinct().order_by('-comments_no', '-publish_date')[:4]
# #     return {'popular_posts': all_popular_post}
#
#
# def media_posts_tag(user):
#     posts = Post.objects.filter(user=user)
#     return {'media_posts': posts}
#
#
# tag_template = get_template('account/user/user-detail-page.html')
# register.inclusion_tag(tag_template)(media_posts_tag)
