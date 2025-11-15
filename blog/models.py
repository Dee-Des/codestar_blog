from django.db import models
from django.contrib.auth.models import User # Import models to connect

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

# A class Meta is useful when you want to add data that is not a database table
# field to your model.
# The ordering option adds metadata to the model about the default order in 
# which the list of posts is displayed.
# The posts are now listed from oldest to newest creation time. The - prefix on 
# created_on indicates the posts are displayed in descending order of creation 
# date. If no leading - is used, then the order is ascending, and if a ? prefix
# is used, then the order is randomised.
    class Meta:
        ordering = ["-created_on"]

    # methhods always below Meta classes.
    # This method gives each post a name that superusers, rather than Python
    # developers, can more easily understand. When we look at posts in the 
    # console or admin panel, this name helps us figure out which post is 
    # which.
    #def __str__(self):
    #    return f"The title of this post is {self.title}"


  # Using the meta option of ordering allows you, as the developer, to define your
  #  preferred default order of the database table contents.
#    f-string that includes both the post title and author in the following format.
    def __str__(self):
        return f"{self.title} | written by {self.author}"
    

# The __str__() dunder method lets you represent your class object as a string
#  for the benefit of your app's user. Keeping this logic in the model prevents 
# you from having to implement it in the view or the template code.

#convention - leave 2 lines between classes
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

# add row-level functionality in Comments objects for logic and metadata 
# handling so as to provide human readable string representation and
# ordering for users.
    class Meta:
        ordering = ["created_on"]


    def __str__(self):
        return f"Comment {self.body} by {self.author}"