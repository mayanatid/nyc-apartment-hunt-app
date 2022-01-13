from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import F, Avg, Sum

HOOD_CHOICES=[
    "Lower East Side",
    "Financial District",
    "Chelsea",
    "West Village",
    "East Village",
    "SoHo",
    "Tribeca",
    "Hell's Kitchen",
    "Midtown",
    "Upper West Side",
    "Flatiron"
]

# Create your views here.

# STILL NEED TO ADD LOGIN CHECK ON HOME
def home(request):
    if request.user.is_authenticated:
        print(request.GET)
        query = request.GET
        hood = query.get("neighborhood")
        order_by = request.GET.get('order_by', 'addDate')
        allListings = None
        if hood:
            allListings = Listing.objects.filter(neighborhood__icontains=hood)
        else:
            hood=""
            allListings=Listing.objects.all() # select * from Listing

        print(hood)

        if order_by=='rating':
            allListings = allListings.annotate(average_rate = (Avg('review__rating_location') + Avg('review__rating_layout') + Avg('review__rating_price'))/3).order_by("-average_rate")
        elif order_by=='addDate':
            allListings = allListings.order_by("-"+order_by)
        else:
            allListings = allListings.order_by(order_by)

        context = {
            "listings":allListings,
            "hood":hood,
            "hood_choices": HOOD_CHOICES
        }

        return render(request, 'main/index.html', context)
    else:
        # if not logged in
        return redirect("accounts:login")

# detail page
def detail(request, id):
    listing = Listing.objects.get(id=id) # select * from listing where id=id
    reviews = Review.objects.filter(listing = id).order_by("-comment")
    print(listing.averageLocation)
    # agg = listing.averageLocation + listing.averageLocation 

    # Not necessary but here from earlier
    average = reviews.aggregate(Avg("rating"))['rating__avg']
    if average == None:
        average = 0
    average = round(average,2)
    context = {
        "listing": listing,
        "reviews": reviews,
        #"average": agg
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

# review listing
def add_review(request, id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data=form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating_location = request.POST["rating_location"]
                data.rating_layout = request.POST["rating_layout"]
                data.rating_price = request.POST["rating_price"]
                data.user = request.user
                data.listing = listing
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, "main/details.html", {"form": form})
    else:
        return redirect("accounts:login")

# edit reviews
def edit_review(request, listing_id, review_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(id=listing_id)
        # review
        review = Review.objects.get(listing=listing, id=review_id)
        #print(review.ratingTotal)

        # check if the review was done by logged on user
        if request.user == review.user:
            # grant permission to edit
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 5) or (data.rating < 0):
                        error = "Out of range. Please select rating from 0 to 5" 
                        return render(request, "main/editreview.html", {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", listing_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {'form': form})
        else:
            return redirect("main:detail", listing_id)
    else:
        return redirect("accounts:login")

# delete reviews
def delete_review(request, listing_id, review_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(id=listing_id)
        # review
        review = Review.objects.get(listing=listing, id=review_id)

        # check if the review was done by logged on user
        if request.user == review.user:
            # grant permission to delete
            review.delete()

        return redirect("main:detail", listing_id)
    else:
        return redirect("accounts:login")