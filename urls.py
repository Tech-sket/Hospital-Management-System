from django.urls import path
from . import views

urlpatterns = [
    path("oauth2/", views.oauth2_start, name="google_oauth_start"),
    path("oauth2callback/", views.oauth2_callback, name="google_oauth_callback"),
]