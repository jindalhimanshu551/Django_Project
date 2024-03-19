import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BaseTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Todo(BaseTime):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def one_day_ago(self):
        return self.created_at <= timezone.now() - datetime.timedelta(days=1)

