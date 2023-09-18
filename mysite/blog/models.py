from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
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
    tags = TaggableManager()

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
        return reverse('blog:post_detail', 
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                        ])

# COMMENT MODEL
class Comment(models.Model):
    """ Defines comment table structure """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    # META PROPS
    class Meta:
        """ Adds meta props to model """
        ordering = ["created_at"]
        indexes = [models.Index(fields=["created_at"])]
    def __str__(self):
        """ Handle string reprs of object """
        return f"Commented by {self.name} on {self.post}"
