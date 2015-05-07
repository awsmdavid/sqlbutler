from django.shortcuts import render
from django.db.models import Q
# from blog.models import __
import string
import urllib


def index(request):
    return render(request, 'blog/index.html')

def faq(request):
    return render(request, 'blog/faq.html')
