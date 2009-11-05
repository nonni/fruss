from django.db import models
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from fruss.shaker.models import PermissionMixIn

class Category(PermissionMixIn):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=100, blank=True)

    instance_permissions = (
            ("can_view_", "Can view "),
            ("can_write_", "Can Write "),
    )

    class Meta:
        verbose_name_plural = "Categories"
        
    def save(self):
        print "IN CATEGORY SAVE"
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    category = models.ForeignKey(Category, related_name="threads")
    title = models.CharField(max_length=200)
    hidden = models.BooleanField(default=False)
    latest_post = models.ForeignKey('Post', related_name="latest_post", null=True)

    class Meta:
        ordering = ['-latest_post__pub_date']

    def has_read(self, user):
        if not UserRead.objects.get_or_create(user=user, thread=self.id)[0].read:
            return False
        else:
            return True

    def __unicode__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, related_name="%(class)s_author")
    body = models.TextField()
    pub_date = models.DateTimeField('Date Published')
    update = models.DateTimeField('Date Updated')
    thread = models.ForeignKey(Thread)
    hidden = models.BooleanField(default=False)
    markdown = models.BooleanField(default=True)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return '%s - %s' % (self.author, self.body[0:10])


class UserRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    read = models.BooleanField(default=False)

