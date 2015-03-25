from django.db import models
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils import simplejson
from collections import Counter, defaultdict
import random
 
# GENDER_CHOICES = (
#     ('Male', 'Male'),
#     ('Female', 'Female'),
# )

class essayData(models.Model):
    # essayId = models.IntegerField(default= lambda: random.randint(10000000,19999999))
    text = models.CharField(max_length=255)

    class Meta:
        ordering = ['-text']

class textForm(ModelForm):
    class Meta:
        model = essayData

# class textForm(models.Model):
#     text = models.CharField(max_length=25500, blank=True, null=True)
#     words = models.CharField(max_length=25500, blank=True, null=True)