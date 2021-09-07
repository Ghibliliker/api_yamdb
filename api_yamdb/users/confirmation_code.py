from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class ConfirmationCodeGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.username)
            + six.text_type(timestamp)
            + six.text_type(user.email)
        )


confirmation_code = ConfirmationCodeGenerator()
