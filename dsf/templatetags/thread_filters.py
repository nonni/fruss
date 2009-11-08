from django import template
from django.utils.translation import ugettext as _

import markdown
from contrib.markdown.extensions.youtube import YouTubeExtension
from contrib.markdown.extensions.mp3player import MP3PlayerExtension

register = template.Library()

@register.filter("post_count")
def thread_post_count(object):
    '''
    Returns the number of posts a thread has
    '''
    return object.post_set.filter(hidden=False).count()

@register.filter("created")
def thread_created(object):
    '''
    Returns when the thread was created
    '''
    try:
        return object.post_set.latest().pub_date
    except:
        return _("Post not found")

@register.filter("author")
def thread_author(object):
    '''
    Returns the thread's author.
    '''
    try:
        return object.post_set.latest().author
    except:
        return _("Post or author not found!")

@register.filter("redchord")
def thread_redchord(object):
    '''
    Returns the first 20 letters of the latest reply
    '''
    try:
        latest = object.post_set.latest()
        return ("%s: %s" % (latest.author, latest.body))[0:20]
    except:
        return _("Post or body not found!")

@register.filter("last_post_id")
def thread_last_post_id(object):
    '''
    ID of the latest reply to a thread.
    '''
    return object.post_set.latest().id

@register.filter("markdown")
def thread_markdown(object):
    '''
    Apply Markdown to text.
    '''
    #Excape HTML tags
    object = object.replace('<', '&lt;').replace('>', '&gt;')
    tube_ext = YouTubeExtension()
    mp3_ext = MP3PlayerExtension()
    md = markdown.Markdown(extensions=[tube_ext,mp3_ext])
    return md.convert(object)
