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

# Will eventually want to add rating field for location, layout, and price
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields= ("comment", "rating_location", "rating_layout", "rating_price")
        # fields= ("comment", "rating")