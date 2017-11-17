from django import template
from ..models import Post, Tag, Me

register = template.Library()


@register.simple_tag
def get_hot_posts():
    return Post.objects.all().order_by('-views')[:5]


@register.simple_tag
def get_recent_posts():
    return Post.objects.all().order_by('-created_time')[:5]


@register.simple_tag
def get_all_tags():
    return Tag.objects.all()


# @register.simple_tag
# def me():
#     return Me.objects.all()
