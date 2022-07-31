from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer