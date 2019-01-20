from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, BaseSerializer

from Final.models import Game, GameComment, UserComment


class GameSerializer(ModelSerializer):
    @staticmethod
    def validate_hold(data):
        numbers = data.split(',')
        try:
            for number in numbers:
                hold = int(number)
                if hold > 6 or hold < 1:
                    raise ValidationError('Hold Value must between 1 and 6')
            return data
        except ValueError:
            raise ValidationError('Unsupported format hold!')

    class Meta:
        model = Game
        fields = ('max_score', 'dice_count', 'hold', 'max_roll', 'name')


class GameActionSerializer(BaseSerializer):
    action = serializers.NullBooleanField(required=True)
    game_id = serializers.CharField(max_length=100)


class GameRateSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'rate')


class GamePlayedCountSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'play_count')


class GameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameComment
        fields = ('text', 'rate', 'user', 'game')


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = ('text', 'rate', 'user', 'to_user')


class GameAcceptCommentSerializer(ModelSerializer):
    game_comment = serializers.ListField()

    class Meta:
        model = GameComment
        fields = ('game_comment',)


class UserAcceptCommentSerializer(ModelSerializer):
    user_comment = serializers.ListField()

    class Meta:
        model = UserComment
        fields = ('user_comment',)
