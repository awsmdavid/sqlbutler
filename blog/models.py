from django.db import models
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils import simplejson
import random, string

class word(models.Model):
    word = models.CharField(max_length=255)
    count = models.IntegerField()
    definition = models.CharField(max_length=255)
    synonyms = models.CharField(max_length=255)
    connotation = models.CharField(max_length=255)
