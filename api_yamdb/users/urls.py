from django.urls import path, include

from rest_framework import routers

from .views import YamdbTokenObtainPairView, UserViewSet, signup

router = routers.DefaultRouter()
router.register(r"signup", UserViewSet)

urlpatterns = [
    # path("auth/signup", signup, name="signup"),
    path("auth/", include(router.urls)),
    path(r"auth/token/", YamdbTokenObtainPairView.as_view()),
]
