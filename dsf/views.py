# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import ThreadForm, ReplyForm
from models import Post, Thread

def get_threads(request):
    
    return render_to_response('dsf/thread_list.html', {'thread_list': Thread.objects.all()})

def get_thread_posts(request, thread_id):
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit = False)
            print reply.__class__
            #TODO: Check if user is logged in
            reply.author = request.user
            reply.thread_id = thread_id
            reply.save()
    else:
        form = ReplyForm()

    post_list = Post.objects.all().filter(id=thread_id)
    p = Paginator(post_list, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = p.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404

    return render_to_response('dsf/thread_detail.html', {'posts': posts, 'form': form})
    


def new_thread(request):
    if request.method == 'POST':
        print 'Request is post'
        form = ThreadForm(request.POST)
        if form.is_valid():
            print 'Form is valid'
            thread = form.save(commit = False)
            #TODO: Check if user is logged in.
            thread.author = request.user
            thread.save()
            return HttpResponseRedirect('/forum/')
    else:
        form = ThreadForm()

    return render_to_response('dsf/thread_new.html', { 'form': form, })
