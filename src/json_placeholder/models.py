from django.db import models


class Post(models.Model):
    userId = models.IntegerField(default=99999942,
                                 help_text="Default value of a possible future UserId, do not change.")
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000)


class Comment(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    body = models.TextField(max_length=5000)
