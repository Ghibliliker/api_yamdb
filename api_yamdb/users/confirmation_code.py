from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils import six
from django.conf import settings


class ConfirmationCodeGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.username)
            + six.text_type(user.email)
            + six.text_type(timestamp)
        )


confirmation_code = ConfirmationCodeGenerator()


def create_code(user):
    return confirmation_code.make_token(user)


def send_email_with_confirmation_code(code, email):
    send_mail(
        'Confirmation code',
        code,
        settings.EMAIL_ADMIN,
        [email],
        fail_silently=False,
    )
