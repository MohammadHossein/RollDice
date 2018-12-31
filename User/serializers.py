import hashlib
import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from User.models import User

logger = logging.getLogger('django')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username:
            if password:
                hash_pass = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()
                try:
                    User.objects.get(password=hash_pass, username=username)
                except Exception as e:
                    logger.log(logging.INFO, e.args)
                    raise ValidationError('incorrect username or password')
                return data
            else:
                raise ValidationError('password cannot be empty')
        else:
            raise ValidationError('username cannot be empty')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photo', 'email', 'birth_date', 'sex', 'password')

    def create(self, validated_data):
        logger.log(logging.INFO, validated_data['password'])
        validated_data['password'] = hashlib.sha512(bytes(validated_data['password'], 'utf-8')).hexdigest()
        return User.objects.create(**validated_data)
