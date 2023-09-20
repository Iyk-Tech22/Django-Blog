""" Define the blog sitemap """
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSiteMap(Sitemap):
    """ Define post sitemap """
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        """ Retrieve post to be map """
        return Post.published.all()
    
    def lastmod(self, obj):
        """  Return the last update of post  """
        return obj.updated_at