from django.db import models
from django.contrib.auth.models import User
from todo.models import BaseTime
from ckeditor.fields import RichTextField


class Blog(BaseTime):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextField()
    is_published = models.BooleanField(default=True)
    image = models.ImageField(upload_to="blog_images", null=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class Comment(BaseTime):
    comment_text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("blog",)

    def __str__(self):
        return self.comment_text[0:13] + "..." + "by " + self.user.username


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    class Meta:
        ordering = ("blog",)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    is_bookmarked = models.BooleanField(default=False)

    class Meta:
        ordering = ("user",)
