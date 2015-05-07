from django.shortcuts import render
from django.db.models import Q
# from blog.models import __
import string
import urllib


def index(request):
    return render(request, 'blog/index.html')

def results(request):
    if request.method == 'POST':
        return render(request, 'blog/results.html', { 'search_results': essay_data})
    return render(request, 'blog/index.html')
