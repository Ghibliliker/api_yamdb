from django.urls import include, path
from rest_framework import routers

from .views import (SignUpViewSet, UsersViewSet, YamdbTokenViewSet,
                    get_confirmation_code, get_me)

router_users = routers.DefaultRouter()
router_users.register(r'users', UsersViewSet, basename='users'),

urlpatterns = [
    path(r'v1/users/me/', get_me, name='me'),
    path(r'v1/auth/signup/', SignUpViewSet.as_view()),
    path(r'v1/auth/token/', YamdbTokenViewSet.as_view()),
    path(r'v1/auth/code/', get_confirmation_code, name='getcode'),
    path(r'v1/', include(router_users.urls)),
]
