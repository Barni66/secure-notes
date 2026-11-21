from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    content = models.TextField()

    secret = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    