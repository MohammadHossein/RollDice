import logging

from rest_framework import serializers

from User.models import User

logger = logging.getLogger('django')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photo', 'email', 'birth_date', 'sex', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

