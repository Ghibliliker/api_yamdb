from django.urls import include, path
from rest_framework import routers

from .views import (SignUpViewSet, UsersViewSet, YamdbTokenViewSet,
                    get_confirmation_code)

router_users = routers.DefaultRouter()
router_users.register(r'users', UsersViewSet, basename='users'),

urlpatterns = [
    path(r'v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    path(r'v1/auth/token/', YamdbTokenViewSet.as_view(), name='token'),
    path(r'v1/auth/code/', get_confirmation_code, name='getcode'),
    path(r'v1/', include(router_users.urls)),
]
