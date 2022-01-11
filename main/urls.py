from django.contrib import admin
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.detail, name='detail'),
    path('addlisting/', views.add_listing, name="add_listing"),
    path('editlisting/<int:id>', views.edit_listing, name="edit_listing"),
    path('deletelisting/<int:id>', views.delete_listing, name="delete_listing")
]
