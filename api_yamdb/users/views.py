from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .confirmation_code import create_code, send_email_with_confirmation_code
from .models import User
from .permissions import GlobalPermission
from .serializers import (UserSerializerForCode, UsersSerializer,
                          YamdbTokenSerializer, MeSerializer)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_confirmation_code(request):
    if ('username' not in request.data) or (request.data['username'] is None):
        return Response(
            {'username': 'is empty'},
            status=status.HTTP_400_BAD_REQUEST)
    user_name = request.data['username']
    if ('email' not in request.data) or (request.data['email'] is None):
        return Response(
            {'email': 'is empty'},
            status=status.HTTP_400_BAD_REQUEST)
    e_mail = request.data['email']
    user = get_object_or_404(User, username=user_name, email=e_mail)
    if user.confirmation_code is None:
        conf_code = create_code(user)
        user.confirmation_code = conf_code
        user.save()
    else:
        conf_code = user.confirmation_code

    send_email_with_confirmation_code(conf_code, user.email)

    return Response(
        {'username': user_name}
    )


class SignUpViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = UserSerializerForCode(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = MeSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)

    @action(
        detail=True,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
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
            user = self.request.user
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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    permission_classes = [GlobalPermission]


class YamdbTokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
