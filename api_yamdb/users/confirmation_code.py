from django.core.mail import send_mail
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


def create_code(user):
    return confirmation_code.make_token(user)


def send_email_with_confirmation_code(code, email):
    send_mail(
        "Confirmation code",
        code,
        "from@example.com",
        [email],
        fail_silently=False,
    )
