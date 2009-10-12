import urllib, hashlib
from django import template
from dsf.models import Post
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
    print token.contents
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
    TODO: make it return an empty string if email has no
          gravatar.
    '''
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id':hashlib.md5(user.email).hexdigest(),
        'size':str(size)})
    return """<img src="%s" alt="gravatar for %s" />""" % (gravatar_url, user.username)

register.simple_tag(gravatar) 
