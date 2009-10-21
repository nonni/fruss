from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()

    def __unicode__(self):
        return self.name

class Thread(models.Model):
    category = models.ForeignKey(Category, related_name="threads")
    title = models.CharField(max_length=200)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, related_name="%(class)s_author")
    body = models.TextField()
    pub_date = models.DateTimeField('Date Published', auto_now=True)
    update = models.DateTimeField('Date Updated', auto_now=True)
    thread = models.ForeignKey(Thread)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return '%s - %s' % (self.author, self.body[0:10])

class UserRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    read = models.BooleanField(default=False)

