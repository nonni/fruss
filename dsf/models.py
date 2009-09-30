from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name

class Thread(models.Model):
    author = models.ForeignKey(User, related_name="threads")
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Date Published', auto_now=True)
    update = models.DateTimeField('Date Updated', auto_now=True)
    category = models.ForeignKey(Category, related_name="threads")

    def __unicode__(self):
        return self.title


