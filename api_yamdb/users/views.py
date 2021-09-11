from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
# from rest_framework_simplejwt.views import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from .models import User
from .serializers import UserSerializerForCode, UserSerializer
from .serializers import YamdbTokenSerializer
# from .permissions import IsRoleAdmin, IsRole


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_confirmation_code(request):
    user_name = request.data["username"]
    e_mail = request.data["email"]
    user = get_object_or_404(User, username=user_name, email=e_mail)
    conf_code = user.confirmation_code
    send_mail(
        "Confirmation code",
        conf_code,
        "from@example.com",
        [e_mail],
        fail_silently=False,
    )

    return Response(
        {"username": user_name}
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerForCode
    permission_classes = (AllowAny,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsRoleAdmin,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination


class YamdbTokenViewSet(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsRole,)

    def post(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(request.user)
            return Response({"token": str(refresh.access_token)})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YamdbCodeViewSet(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsRole,)

    def get(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"username": serializer.username}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
