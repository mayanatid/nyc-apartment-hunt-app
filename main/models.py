from djmoney.models.fields import MoneyField
from phone_field import PhoneField
from django.utils import timezone
from django.db import models

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
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='USD')
    averageRating = models.FloatField(default=0)
    addDate = models.DateTimeField(default=timezone.now)
    phoneNumber = PhoneField(blank=True, help_text='Contact phone number')
    image = models.URLField(default=None, null=True)
    #image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


