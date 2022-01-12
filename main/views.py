from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    allListings=Listing.objects.all() # select * from Listing
    context = {
        "listings":allListings,
    }

    return render(request, 'main/index.html', context)

# detail page
def detail(request, id):
    listing = Listing.objects.get(id=id) # select * from listing where id=id

    context = {
        "listing": listing
    }
    return render(request, 'main/details.html', context)

# add listing to database
def add_listing(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = ListingForm(request.POST or None)

                # Check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = ListingForm()
            return render(request, 'main/addlisting.html', {"form": form, "controller": "Add Listing"})
        
        # if not admin
        else:
            return redirect("main:home")

    # if not logged in
    return redirect("accounts:login")


# edit listing
def edit_listing(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the listing linked with id
            listing = Listing.objects.get(id=id)

            # form check
            if request.method == "POST":
                form = ListingForm(request.POST or None, instance=listing)
                # Check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = ListingForm(instance=listing) 
            return render(request, 'main/addlisting.html', {"form": form, "controller": "Edit Listing"})
        # if not admin
        else:
            return redirect("main:detail", id)

    # if not logged in
    return redirect("accounts:login")



# delete listing
def delete_listing(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:    
            # Get listing
            listing = Listing.objects.get(id=id)

            # delete the listing
            listing.delete()
            return redirect("main:home")
        else:
            return redirect("main:detail", id)
            
    # if not logged in
    return redirect("accounts:login")
