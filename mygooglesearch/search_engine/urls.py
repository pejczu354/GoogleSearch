from django.urls import path

from . import views

urlpatterns = [
    path('get_configuration_data/', views.get_configuration_data, name="get_configuration_data"),
    path('set_configure_data/', views.set_configure_data, name="set_configure_data"),
    path('get_data/', views.get_data, name="get_data"),
]