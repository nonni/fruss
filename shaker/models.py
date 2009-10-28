from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

class PermissionMixIn(models.Model):
    
    def save(self, *args, **kwargs):
         if not self.id and hasattr(self, 'instance_permissions'):
             for perm in self.instance_permissions:
                p = Permission()
                p.codename = '%s%s' % (perm[0], self.slug)
                p.name = '%s%s' % (perm[1], self.name)
                p.content_type = ContentType.objects.get_for_model(self)
                p.save()
        return super(PermissionMixIn, self).save(*args, **kwargs)

    class Meta:
        abstract = True
