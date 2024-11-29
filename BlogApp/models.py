from django.db import models
from administration.models import Account
class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    postId = models.AutoField(primary_key=True)
    postTitle = models.CharField(max_length=250)
    postContent = models.TextField()
    image = models.ImageField(upload_to='home/wadmin/Downloads/BlogSiteAPP/BlogApp/static/jpeg/Posts/', blank=True, null=True)  # Use a more generic path
    postDate = models.DateTimeField(auto_now_add=True)
    postEditDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.postTitle