from django.urls import path, include

from rest_framework import routers

from .views import SignUpViewSet, UsersViewSet, get_confirmation_code, get_me
from .views import YamdbTokenViewSet

"""router_auth = routers.DefaultRouter()
router_auth.register(r"signup", SignUpViewSet.as_view(), basename="signup")"""

router_users = routers.DefaultRouter()
router_users.register(r"users", UsersViewSet, basename="users"),

urlpatterns = [
    path(r"users/me/", get_me, name="me"),
    # path(r"auth/", include(router_auth.urls)),
    path(r"auth/signup/", SignUpViewSet.as_view()),
    path(r"auth/token/", YamdbTokenViewSet.as_view()),
    path(r"auth/code/", get_confirmation_code, name="getcode"),
    path(r"", include(router_users.urls)),
]
