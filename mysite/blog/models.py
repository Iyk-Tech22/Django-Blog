from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# CUSTOME MODEL MANAGER
class PublishManager(models.Manager):
    """ 
        Define a custome manager that
        retrieves objs with status set to published
    """
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """ Post model map to table in a db """
    
    objects = models.Manager()
    published = PublishManager()

    class Status(models.TextChoices):
        """ Use to define the status or state of a blog post """
        DRAFT = "DF", "DRAFT"
        PUBLISHED = "PB", "PUBLISHED"


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    # DEFINE METADATA FOR OUR MODEL
    class Metal:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        """ Canonical url for post data """
        return reverse("blog:post_detail", args=[
            self.publish__year,
            self.publish_month,
            self.publish_day,
            self.slug
        ])
        
    
