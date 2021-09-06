from rest_framework_simplejwt.views import TokenObtainPairView

from serializers import YamdbTokenObtainPairSerializer


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer
