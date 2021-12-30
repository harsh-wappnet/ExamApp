from django.urls import path

from .views import health_check, populate_data, get_data

urlpatterns = [
    path("check/", health_check, name="health_check"),
    path("populate/db/", populate_data, name="populate_data"),
    path("get/data/", get_data, name="get_data"),
]
