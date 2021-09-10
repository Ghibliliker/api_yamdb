from django.urls import path, include

from rest_framework import routers

# from .views import YamdbTokenObtainPairView, UserViewSet, signup
from .views import UserViewSet, UsersViewSet, get_confirmation_code
from .views import YamdbTokenViewSet

router = routers.DefaultRouter()
router.register(r"signup", UserViewSet)

urlpatterns = [
    path(r"auth/code/", get_confirmation_code, name="getcode"),
    path(r"users/(?P<username>[\w.@+-]+)/", UsersViewSet),
    path(r"users/", UsersViewSet.as_view({"get": "list"})),
    path(r"auth/", include(router.urls)),
    path(r"auth/token/", YamdbTokenViewSet.as_view()),
]
