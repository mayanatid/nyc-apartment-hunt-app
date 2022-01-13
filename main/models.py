from djmoney.models.fields import MoneyField
from phone_field import PhoneField
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Potentially for auto-complete
HOOD_CHOICES=(
    ("Lower East Side", "Lower East Side"),
    ("Financial District", "Financial District"),
    ("Chelsea", "Chelsea"),
    ("West Village", "West Village"),
    ("East Village", "East Village"),
    ("SoHo", "SoHo"),
    ("Tribeca", "Tirbeca"),
    ("Hell's Kitchen", "Hell's Kitchen"),
    ("Midtown", "Midtown"),
    ("Upper West Side", "Upper West Side"),
    ("Flatiron", "Flatiron")
)

# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField(max_length=300)
    neighborhood = models.CharField(max_length=300, choices=HOOD_CHOICES)
    beds = models.IntegerField()
    baths = models.IntegerField()
    #price = MoneyField(max_digits=14, decimal_places=0, default_currency='USD')
    price = models.FloatField(default=0)
    # averageRating = models.FloatField(default=0)
    addDate = models.DateTimeField(default=timezone.now)
    phoneNumber = PhoneField(blank=True, help_text='Contact phone number')
    image = models.URLField(default=None, null=True)
    #image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name

    @property
    def averageLocation(self):
        average = self.review_set.aggregate(Avg("rating_location"))['rating_location__avg']
        if average == None:
            average = 0
        average = round(average,2)
        return average

    @property
    def averageLayout(self):
        average = self.review_set.aggregate(Avg("rating_layout"))['rating_layout__avg']
        if average == None:
            average = 0
        average = round(average,2)
        return average

    @property
    def averagePrice(self):
        average = self.review_set.aggregate(Avg("rating_price"))['rating_price__avg']
        if average == None:
            average = 0
        average = round(average,2)
        return average

    @property
    def totalAverage(self):
        average = (self.averageLocation + self.averageLayout + self.averagePrice)/3
        if average == None:
            average = 0
        average = round(average,2)
        return average



class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, default="No Comment")
    rating = models.FloatField(default=0)
    rating_location = models.FloatField(default=0)
    rating_layout = models.FloatField(default=0)
    rating_price = models.FloatField(default=0)


    def __str__(self):
        return self.user.username

    @property
    def ratingTotal(self):
        average = (self.rating_location + self.rating_layout + self.rating_price)/3
        if average == None:
            average = 0
        average = round(average,2)
        return average