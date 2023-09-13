from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    """ Post model map to table in a db """

    class Status(models.TextChoices):
        """ Use to define the status or state of a blog post """
        DRAFT = "DF", "DRAFT"
        PUBLISHED = "PB", "PUBLISHED"


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    # DEFINE METADATA FOR OUR MODEL
    class Metal:
        ordering = ["-published"]
        indexes = [
            models.Index(fields=["-pubblished"])
        ]
    def __str__(self):
        return self.title
        
    
