from django.db import models
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils import simplejson
from collections import Counter, defaultdict
 
# GENDER_CHOICES = (
#     ('Male', 'Male'),
#     ('Female', 'Female'),
# )

class textForm(forms.Form):
    text = forms.CharField(max_length=255)

class searchResults(models.Model):
    text = models.CharField(max_length=255)

# class textForm(models.Model):
#     text = models.CharField(max_length=25500, blank=True, null=True)
#     words = models.CharField(max_length=25500, blank=True, null=True)