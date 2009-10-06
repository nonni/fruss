from django import template
register = template.Library()

@register.filter("post_count")
def thread_post_count(object):
    return object.post_set.count()

@register.filter("created")
def thread_created(object):
    try:
        return object.post_set.latest().pub_date
    except:
        return "Post not found"

@register.filter("author")
def thread_author(object):
    try:
        return object.post_set.latest().author
    except:
        return "Post or author not found!"

@register.filter("redchord")
def thread_redchord(object):
    try:
        return object.post_set.latest().body[0:20]
    except:
        return "Post or body not found!"
