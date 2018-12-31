import hashlib
import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from User.models import User

logger = logging.getLogger('django')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username:
            if password:
                hash_pass = hashlib.sha512(password)
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
