from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path("auth/", views.obtain_auth_token, name="auth"),
    path("fakeapi/v1/", include("fakeapi.urls")),
    path("admin/", admin.site.urls),
]
