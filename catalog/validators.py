from django.core.exceptions import ValidationError


def validate_sequence_number(value):
    if value < 1:
        raise ValidationError(
            'Sequence number should be greater than or equal to 1'
        )
