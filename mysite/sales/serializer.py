from rest_framework import serializers
from .models import LoginUser, User, Pays, Commodities, ShoppingCart
import uuid


class CustomUUIDField(serializers.UUIDField):
    def to_representation(self, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginUser
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pays
        fields = "__all__"


class CommoditiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commodities
        fields = "__all__"


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = "__all__"
