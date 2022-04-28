from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    header = models.CharField(max_length=200, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(editable=True, null=True, blank=True)
    isDone = models.BooleanField(default=False)
    doneAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isOverDued = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.header)
