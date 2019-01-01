from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from Final.models import Game


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
        fields = ('max_score', 'dice_count', 'hold', 'max_roll')
