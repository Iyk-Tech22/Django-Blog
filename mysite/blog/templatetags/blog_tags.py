"""
Implement a custome template tag
"""
from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown


register = template.Library()

# CUSTOME TEMPLATE TAGS
@register.simple_tag
def total_posts():
    """ Counts number blog post """
    return Post.published.count()
    
@register.inclusion_tag("blog/post/latest.html")
def latest_posts(count=5):
    """ Get latest posts """
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts":latest_posts}
        
@register.simple_tag
def get_most_commented_posts(count=5):
    """ Return most comment posts """
    return Post.published.annotate(
        total_comments=Count("comments")
    ).order_by("-total_comments")[:count]
        
# CUSTOME TEMPLATE FILTERS
@register.filter(name="markdown")
def markdown_to_html(text):
    """ Converts markdown to html """
    return mark_safe(markdown(text))