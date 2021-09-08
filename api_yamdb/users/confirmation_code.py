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


def send_email_with_confirmation_code(user):
    conf_code = confirmation_code.make_token(user)
    send_mail(
        "Confirmation code",
        conf_code,
        "from@example.com",
        [user.e_mail],
        fail_silently=False,
    )
