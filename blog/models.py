from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    headline = models.CharField(max_length=40)
    text = models.TextField()
    date_published = models.DateTimeField()
    pos_marks = models.IntegerField(default=0)
    neg_marks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # author = models.CharField(max_length=40, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=140)
    date_published = models.DateTimeField()
    pos_marks = models.IntegerField(default=0)
    neg_marks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
