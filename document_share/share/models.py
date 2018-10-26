from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    owner = models.CharField(max_length=50, null=True, blank=True)
    upload_date = models.DateField(null=True, blank=True)
    users = models.ManyToManyField(User)
