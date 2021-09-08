from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from .models import User
from .serializers import UserSerializer
from .serializers import YamdbTokenObtainPairSerializer
from .confirmation_code import confirmation_code
# from .permissions importIsAuthenticatedAndAuthor,IsAuthorOrReadOnlyPermission
# from .permissions import ReadOnly


@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_name = request.data["username"]
        e_mail = request.data["email"]
        instance = serializer.save(username=user_name, email=e_mail)
        conf_code = confirmation_code.make_token(instance)
        send_mail(
            "Confirmation code",
            conf_code,
            "from@example.com",
            [e_mail],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def create(self, request):
        user_name = request.data["username"]
        e_mail = request.data["email"]
        serializer.save(username=user_name, email=e_mail)


"""
    def perform_create(self, serializer):
        print(self)
        user_name = self.data["username"]
        e_mail = self.data["email"]
        serializer.save(username=user_name, email=e_mail)
        conf_code = confirmation_code.make_token(instance)
        send_mail(
            "Confirmation code",
            conf_code,
            "from@example.com",
            [e_mail],
            fail_silently=False,
        )
"""


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer
