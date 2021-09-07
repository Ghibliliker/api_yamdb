from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer
from .serializers import YamdbTokenObtainPairSerializer
from .confirmation_code import confirmation_code
# from .permissions importIsAuthenticatedAndAuthor,IsAuthorOrReadOnlyPermission
# from .permissions import ReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        user_name = self.kwargs["username"]
        user_email = self.kwargs["email"]
        instance = serializer.save(username=user_name, email=user_email)
        conf_code = confirmation_code.make_token(instance)
        send_mail(
            "Confirmation code",
            conf_code,
            "from@example.com",
            instance.email,
            fail_silently=False,
        )


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer
