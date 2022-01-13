from django.contrib import admin
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.detail, name='detail'),
    path('addlisting/', views.add_listing, name="add_listing"),
    path('editlisting/<int:id>', views.edit_listing, name="edit_listing"),
    path('deletelisting/<int:id>', views.delete_listing, name="delete_listing"),
    path('addreview/<int:id>', views.add_review, name="add_review"),
    path('editreview/<int:listing_id>/<int:review_id>/', views.edit_review, name="edit_review"),
    path('deletereivew/<int:listing_id>/<int:review_id>/', views.delete_review, name="delete_review")
]
