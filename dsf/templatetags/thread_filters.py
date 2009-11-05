from django import template
from django.utils.translation import ugettext as _

import markdown
from contrib.markdown.extensions.youtube import YouTubeExtension

register = template.Library()

@register.filter("post_count")
def thread_post_count(object):
    return object.post_set.filter(hidden=False).count()

@register.filter("created")
def thread_created(object):
    try:
        return object.post_set.latest().pub_date
    except:
        return _("Post not found")

@register.filter("author")
def thread_author(object):
    try:
        return object.post_set.latest().author
    except:
        return _("Post or author not found!")

@register.filter("redchord")
def thread_redchord(object):
    try:
        latest = object.post_set.latest()
        return ("%s: %s" % (latest.author, latest.body))[0:20]
    except:
        return _("Post or body not found!")

@register.filter("last_post_id")
def thread_last_post_id(object):
    return object.post_set.latest().id

@register.filter("markdown")
def thread_markdown(object):
    myext = YouTubeExtension()
    md = markdown.Markdown(extensions=[myext])
    return md.convert(object)
