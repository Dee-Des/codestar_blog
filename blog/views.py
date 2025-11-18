from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm

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
    if request.method == "POST":
        print("Received a POST request")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    comment_form = CommentForm(data=request.POST)
    print("About to render template")

    return render(
    request,
    "blog/post_detail.html",
    {"post": post,
    "comments": comments,
    "comment_count": comment_count,
    "comment_form": comment_form,
    "coder": "Matt Rudge"},
     )

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))