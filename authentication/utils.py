# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type


# class AppTokenGenerator(PasswordResetTokenGenerator):

#     def _make_hash_value(self, user, timestamp):
#         return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


# account_activation_token = AppTokenGenerator()

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.is_active}{user.pk}{timestamp}{user.last_login}"

account_activation_token = AppTokenGenerator()
