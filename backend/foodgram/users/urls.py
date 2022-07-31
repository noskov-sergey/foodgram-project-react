from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet


app_name = 'users'


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
