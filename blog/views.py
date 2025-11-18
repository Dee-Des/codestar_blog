from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    # can now leave some posts in Draft while finish them and they will not show
    #on the live blog
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6
    # to display all of the objects, or records, from the Post model.by all users
   # queryset = Post.objects.all()

    #to display only the objects, or records (blog posts here) by second user created
    #queryset = Post.objects.filter(author=2)
    #template_name = "post_list.html"

    # another method we can use is order_by
    # order_by allows us to specify the ordering of our records
    # to display all of our post s ordered from teh earliest date
    # to the most recent, we could use this:
    # queryset = Post.objects.all().order_by("created_on")

    # To reverse the order, put a minus sign in front of the field 
    # name. 
    # So, to order in descending order - from most recent to earliest, 
    # which is the most sensible way of ordering blog posts, we would use:
    # Post.objects.all().order_by("-created_on")
    # the ordering works with filters too


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    return render(
    request,
    "blog/post_detail.html",
    {"post": post,
    "comments": comments,
    "comment_count": comment_count,
    "coder": "Matt Rudge"},
     )
