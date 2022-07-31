from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов, модели Tag."""

    class Meta:
        model = User
        fields = ('__all__')