from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from collections import Counter, defaultdict
import string
import operator

def index(request):
	return render(request, 'blog/index.html')


def splitText(text):
    return text.split()

def removePunc(text):
    #syntax translate(find text (mapper), text to replace)
    return text.translate(string.maketrans("",""), string.punctuation)

def countWords(list):
    return Counter(list)

def taketextandcount(text):
    return splitText(removePunc(text))


def sender(request):
    if form.is_valid():
        cd = form.cleaned_data
        letter = cd['post']
        request.session['post_data'] = letter
        next = reverse('new_view',)
        return HttpResponseRedirect(next)


def new_view(request,):
    post_data = request.session.get('post_data')
    return render(request, 'new_view.html', {'post': post})