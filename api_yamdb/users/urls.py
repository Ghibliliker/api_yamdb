from django.urls import path, include

from rest_framework import routers

from .views import YamdbTokenObtainPairView, UserViewSet

router = routers.DefaultRouter()
router.register(r"signup", UserViewSet)

urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/token/", YamdbTokenObtainPairView.as_view()),
]
