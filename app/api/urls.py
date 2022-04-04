from django.urls import path
from . import views

urlpatterns = [
    path('api/exchangerates', views.getCurrenciesData),
    path('api/', views.apiInformation),
]