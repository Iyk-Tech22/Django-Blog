"""
    Generate RSS Feed for user to consume
"""
from markdown import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    """ Handle generating for feed for recent posts """
    
    title = "My Blog Post"
    link = reverse_lazy("blog:post_list")
    description = "New Blog Post"

    def items(self):
        """ Return posts to consume by RSS aggregetor """
        return Post.published.all()[:5]
    
    def item_title(self, item):
        """ Define RSS post title """
        return item.title

    def title_description(self, item):
        """ Define RSS post description """
        return truncatewords_html(markdown(item.body), 30)
    
    def title_pubdate(self, item):
        """ Define RSS post publish date """
        return item.publish
    
    
    