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

# AGE_CHOICES = (
#     ('age_1', '0-5'),
#     ('age_2', '6-13'),
#     ('age_3', '14-20'),
#     ('age_4', '21-34'),
#     ('age_5', '35-59'),
#     ('age_6', '60+'),
# )

# PRICE_CHOICES = (
#     ('price_1', '$0-20'),
#     ('price_2', '$20-50'),
#     ('price_3', '$50-100'),
#     ('price_4', '$100+'),    
# )

class Text(models.Model):
    text = models.CharField(max_length=25500, blank=True, null=True)
    words = models.CharField(max_length=25500, blank=True, null=True)