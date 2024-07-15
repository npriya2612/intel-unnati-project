# telemetry_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example index path
    path('collect_data/', views.collect_data, name='collect_data'),
    path('telemetry_results/', views.telemetry_results, name='telemetry_results'),
    path('previous-data/', views.previous_data_view, name='previous_data'),
    path('power-utilization/', views.power_utilization, name='power_utilization'),

    # Add more paths as per your application's requirements
]
