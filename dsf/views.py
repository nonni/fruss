# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from forms import ThreadForm

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
