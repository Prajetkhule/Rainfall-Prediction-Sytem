from django.urls import path
from . import views

urlpatterns = [
    path('rain_dataset', views.rain_dataset, name='rain_dataset'),
    path('rain_export_to_csv', views.rain_export_to_csv, name='rain_export_to_csv'),
    path('rain_predict', views.rain_predict, name='rain_predict'),
    path('rainfall_data/<int:pk>', views.rainfall_data, name='rainfall_data'),
]
