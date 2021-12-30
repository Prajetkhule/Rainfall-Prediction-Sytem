from django.urls import path
from . import views

urlpatterns = [
    path('regions/', views.regions, name = "regions"),
    path('states/', views.states, name = "states"),
]
