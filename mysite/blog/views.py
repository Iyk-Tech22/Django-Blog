from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import Post
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

# FUNCTIONAL BASE VIEWS HERE
def post_list(request):
    """ Display all posts """
    post_list = Post.published.all()
    # Pagination
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "posts":posts
    }
    return render(request, "blog/post/list.html", context)
    
def post_detail(request, year, month, day, slug):
    """ Display Post Each Post Details """

    # try:
    #     post = Post.published.get(
    #        publish__year = year,
    #        publish__month = month,
    #        publish__day = day,
    #        slug = post
    #     )
    #    
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found")

    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug
    )
    context = {"post":post}
    return render(request, "blog/post/detail.html", context)

def post_share(request, post_id):
    """ Handle displaying of form, form submmison and emailing """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Send mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email="admin@admin.com", recipient_list=["iyktech09@gmail.com"])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        "post":post,
        "form":form,
        "sent":sent
    }
    return render(request, "blog/post/share.html", context)


#----------------------------------------------------------------#

# CLASS BASE VIEWS HERE
class PostListView(ListView):
    """ Class base view for handling display of all posts """
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
