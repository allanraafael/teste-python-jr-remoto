from django.urls import path, include

urlpatterns = [
    path("", include("api.urls"), name="api"),
]
