from django import forms
from django.forms import fields
from .models import *

# listing add form
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('name', 
                  'neighborhood', 
                  'beds', 
                  'baths',
                  'price',
                  'link',
                  'image')