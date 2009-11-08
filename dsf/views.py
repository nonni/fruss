# Create your views here.
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from models import Thread, Post, Category, UserRead
from forms import ThreadForm, ReplyForm
import markdown

@login_required
def get_threads(request, category=None):
    '''
    Returns a list of all threads in a given category. Paginated.
    If no category is specified, it returns a list of threads from
    all categories.
    '''
    if category is None:
        thread_list = Thread.objects.all().filter(hidden=False)
    else:
        category_id = get_object_or_404(Category, slug=category).id
        thread_list = Thread.objects.all().filter(category=category_id, hidden=False)

    p = Paginator(thread_list, 5) #5 threads each page
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        threads = p.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404

    cats = Category.objects.all()

    return render_to_response('dsf/thread_list.html', {'threads': threads, 'categories': cats, 'category': category}, context_instance=RequestContext(request))

@login_required
def get_thread_posts(request, thread_id):
    '''
    Returns all posts in a thread, including the 'thread' post itself.
    '''
    thread = get_object_or_404(Thread, pk=thread_id)
    if thread.hidden:
        raise Http404 

    #Mark thread a read for user.
    read = UserRead.objects.get_or_create(user=request.user, thread=thread_id)[0]
    read.read = True
    read.save()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit = False)

            #TODO: Check if user is logged in
            reply.author = request.user
            reply.thread_id = thread_id
            reply.pub_date = datetime.now()
            reply.update = datetime.now()
            reply.save()
            thread.latest_post = reply
            thread.save()
            form = ReplyForm() #Clear the form
            #Mark thread as unread for other users
            ur = UserRead.objects.all().filter(thread__exact=thread_id).exclude(user=request.user)
            for u in ur:
                u.read = False
                u.save()
            #Focus on new post after reply.
            return HttpResponseRedirect('%s?page=last#post_%s' % (reverse('thread', args=[thread.id]), reply.id))
    else:
        form = ReplyForm()

    post_list = Post.objects.all().filter(thread=thread_id, hidden=False)
    p = Paginator(post_list, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = p.num_pages
    try:
        posts = p.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    return render_to_response('dsf/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form}, context_instance=RequestContext(request))
    

@login_required
def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            body = data['body']
            thread = Thread.objects.create(title=data['title'], category=data['category'])
            post = Post.objects.create(author=request.user, thread=thread, body=body, pub_date=datetime.now(), update=datetime.now(), markdown=data['markdown'])
            post.save()
            thread.author = request.user
            thread.latest_post = post
            thread.save()
            #Mark thread a read for user.
            read = UserRead.objects.get_or_create(user=request.user, thread=thread)[0]
            read.read = True
            read.save()
            return HttpResponseRedirect(reverse('threads'))
    else:
        form = ThreadForm()

    return render_to_response('dsf/thread_new.html', { 'form': form, })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user is post.author and not request.user.is_superuser:
        return HttpResponse('Access denied!')
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            body = data['body']
            post = get_object_or_404(Post, pk=post_id)
            post.body = body
            post.markdown = data['markdown']
            post.update = datetime.now()
            post.save()
            return HttpResponse(markdown.markdown(post.body))
    if request.user.is_superuser or post.author is request.user:
        form = ReplyForm(post.__dict__)
        return render_to_response('dsf/post_edit.html', {'form':form, 'post_id':post_id})
    else:
        return HttpResponse(_('Access denied!'))

@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponse(markdown.markdown(post.body))

@login_required
def hide_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_superuser or post.author is request.user:
        post.hidden = True
        th = post.thread
        if post == th.post_set.all()[0]:
            th.hidden = True
            th.save()
        post.save()
        return HttpResponse(_('Success'))
    else:
        return HttpResponse(_('Access denied!'))

@login_required
def set_read(request, thread_id):
    #Mark thread a read for user.
    read = UserRead.objects.get_or_create(user=request.user, thread=thread_id)[0]
    read.read = True
    read.save()
    return HttpResponse(_('Success'));
