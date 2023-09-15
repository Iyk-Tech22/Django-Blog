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
    
def post_detail(request, id):
    """ Display Post Each Post Details """
    try:
        post = Post.published.get(id=id)
        context = {"post":post}
    except Post.DoesNotExist:
        raise Http404("No Post Found")
    return render(request, "blog/post/detail.html", context)