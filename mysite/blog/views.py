from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import Post, Comment
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# FUNCTIONAL BASE VIEWS HERE
def post_list(request, tag_slug=None):
    """ Display all posts """
    
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
        "posts":posts,
        "tag":tag,
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
    comments = post.comments.filter(active=True)
    post_tags_id = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id)\
                                       .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tag=Count("tags"))\
                                         .order_by("-same_tag", "-publish")[:4]
    form = CommentForm()
    context = {"post":post, "comments":comments, "form":form, "similar_posts":similar_posts}
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

@require_POST
def post_comment(request, post_id):
    """ Handle comment submmisions """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
       "post":post,
       "form":form,
       "comment":comment
    }
    return render(request, "blog/post/comment.html", context)
    

#----------------------------------------------------------------#

# CLASS BASE VIEWS HERE
class PostListView(ListView):
    """ Class base view for handling display of all posts """
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
