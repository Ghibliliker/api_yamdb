from django.urls import include, path
from rest_framework import routers

from .views import (SignUpViewSet, UsersViewSet, YamdbTokenViewSet,
                    get_confirmation_code, get_me)

router_users = routers.DefaultRouter()
router_users.register(r'users', UsersViewSet, basename='users'),

urlpatterns = [
    path(r'users/me/', get_me, name='me'),
    path(r'auth/signup/', SignUpViewSet.as_view()),
    path(r'auth/token/', YamdbTokenViewSet.as_view()),
    path(r'auth/code/', get_confirmation_code, name='getcode'),
    path(r'', include(router_users.urls)),
]
