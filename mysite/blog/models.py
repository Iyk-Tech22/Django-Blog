from django.db import models
from 
# Create your models here.

class Post(models.Model):
    """ Post model map to table in a db """
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField()
    
    def __str__(self):
        return self.title
        
    
