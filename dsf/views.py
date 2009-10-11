# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from forms import ThreadForm, ReplyForm
from models import Post, Thread

@login_required
def get_threads(request):
    '''
    Returns a list of all threads. Paginated.
    '''
    thread_list = Thread.objects.all().order_by('-pk')
    p = Paginator(thread_list, 5) #5 threads each page
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        threads = p.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404

    print dir(threads)
    return render_to_response('dsf/thread_list.html', {'threads': threads})

@login_required
def get_thread_posts(request, thread_id):
    '''
    Returns all posts in a thread, including the 'thread' post itself.
    '''
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit = False)
            #TODO: Check if user is logged in
            reply.author = request.user
            reply.thread_id = thread_id
            reply.save()
    else:
        form = ReplyForm()

    thread = get_object_or_404(Thread, pk=thread_id)
    post_list = Post.objects.all().filter(thread=thread_id)
    p = Paginator(post_list, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = p.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    return render_to_response('dsf/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})
    

@login_required
def new_thread(request):
    if request.method == 'POST':
        print 'Request is post'
        form = ThreadForm(request.POST)
        if form.is_valid():
            print 'Form is valid'
            data = form.cleaned_data
            #TODO: Check if user is logged in.
            thread = Thread.objects.create(title=data['title'], category=data['category'])
            post = Post.objects.create(author=request.user, thread=thread, body=data['body'])
            thread.author = request.user
            thread.save()
            return HttpResponseRedirect('/forum/')
    else:
        form = ThreadForm()

    return render_to_response('dsf/thread_new.html', { 'form': form, })
