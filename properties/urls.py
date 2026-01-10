from django.urls import path
from properties.views import property_list, get_metrics

urlpatterns = [
    path('properties/', property_list, name='property-list'),
    path('cache/metrics/', get_metrics, name='cache-metrics')
]