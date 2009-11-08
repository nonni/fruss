import urllib, hashlib
from django import template
from dsf.models import Post, UserRead
register = template.Library()

class PostNode(template.Node):
    def __init__(self, thread_id, varname):
        self.thread_id = template.Variable(thread_id)
        self.varname = varname

    def render(self, context):
        try:
            actual_thread_id = self.thread_id.resolve(context)
            context[self.varname] = Post.objects.all().filter(thread=actual_thread_id)[0]
        except template.VariableDoesNotExist:
            return '' 
        return ''

def do_get_thread_post(parser, token):   
    '''
    Returns the thread 'reply' as an object.
    '''
    tokens = token.split_contents()
    if len(tokens) != 4:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments"
    if tokens[2] != 'as':
        raise template.TemplateSyntaxError, "%r second argument must be 'as'"
    return PostNode(tokens[1], tokens[3])

register.tag('get_thread_post', do_get_thread_post)

def gravatar(user, size=60):
    '''
    Returns a gravatar for a given user.
    '''
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id':hashlib.md5(user.email).hexdigest(),
        'size':str(size)})
    return """<img src="%s" alt="gravatar for %s" />""" % (gravatar_url, user.username)

register.simple_tag(gravatar)

def user_has_read(user, thread):
    '''
    Returns True if user has 'read' a thread,
    false if the user has not read it.
    '''
    if not UserRead.objects.get_or_create(user=user, thread=thread)[0].read:
        return "Unread "
    else:
        return ""
        
register.simple_tag(user_has_read)

def have_read(user, thread):
    '''
    Returns an ajax link if user has not 'read' a thread,
    nothing if user has read it.
    '''
    if not UserRead.objects.get_or_create(user=user, thread=thread)[0].read:
        return '<div id="read_%s" style="float:right">read</div>' % thread.id
    else:
        return ''

register.simple_tag(have_read)
