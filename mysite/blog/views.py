from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Post
from django.template import loader

# Create your views here.
def post_list(request):
    """ Display all posts """
    posts = Post.published.all()
    
    context = {
        "posts":posts
    }
    return render(request, "blog/post/list.html", context)
    
def post_detail(request, year, month, day, post):
    """ Display Post Each Post Details """
    try:
        post = Post.published.get(
           publish__year = year,
           publish__month = month,
           publish__day = day,
           slug = post
        )
        context = {"post":post}
    except Post.DoesNotExist:
        raise Http404("No Post Found")
    return render(request, "blog/post/detail.html", context)