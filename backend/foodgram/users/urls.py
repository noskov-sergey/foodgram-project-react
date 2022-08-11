from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import FoodgramUserViewSet

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', FoodgramUserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
