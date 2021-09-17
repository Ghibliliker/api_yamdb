from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .confirmation_code import create_code, send_email_with_confirmation_code
from .models import User
from .permissions import GlobalPermission, MePermission
from .serializers import (
    UserSerializerForCode,
    UsersSerializer,
    YamdbTokenSerializer,
    ConfirmationCodeSerializer
)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    )
    if user.confirmation_code is None:
        conf_code = create_code(user)
        user.confirmation_code = conf_code
        user.save()
    else:
        conf_code = user.confirmation_code

    send_email_with_confirmation_code(conf_code, user.email)

    return Response({'Check your email'})


class SignUpViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializerForCode(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    permission_classes = [GlobalPermission]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[MePermission],
    )
    def me(self, request):

        user = self.request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class YamdbTokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})
