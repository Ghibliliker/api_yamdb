from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .confirmation_code import create_code, send_email_with_confirmation_code
from .models import User
from .permissions import IsRoleAdmin, IsRoleAdminOrSuperUser
from .serializers import (UserSerializerForCode, UsersSerializer,
                          YamdbTokenSerializer)


@api_view(['GET', 'PATCH'])  # noqa: C901
@permission_classes((IsAuthenticated,))  # noqa: C901
def get_me(request):  # noqa: C901
    if request.method == 'GET':  # noqa: C901
        user = request.user  # noqa: C901

        return Response(  # noqa: C901
            {  # noqa: C901
                'username': user.username,  # noqa: C901
                'email': user.email,  # noqa: C901
                'first_name': user.first_name,  # noqa: C901
                'last_name': user.last_name,  # noqa: C901
                'bio': user.bio,  # noqa: C901
                'role': user.role,  # noqa: C901
            }  # noqa: C901
        )  # noqa: C901

    if request.method == 'PATCH':  # noqa: C901
        user = request.user  # noqa: C901
        if 'username' in request.data:  # noqa: C901
            if user.username != request.data['username']:  # noqa: C901
                if not User.objects.filter(  # noqa: C901
                    username=request.data['username']  # noqa: C901
                ) is None:  # noqa: C901
                    return Response(  # noqa: C901
                        {'username': request.data['username']},  # noqa: C901
                        status=status.HTTP_400_BAD_REQUEST  # noqa: C901
                    )  # noqa: C901
            user.username = request.data['username']  # noqa: C901

        if 'email' in request.data:  # noqa: C901
            if user.email != request.data['email']:  # noqa: C901
                if not User.objects.filter(  # noqa: C901
                    email=request.data['email']  # noqa: C901
                ) is None:  # noqa: C901
                    return Response(  # noqa: C901
                        {'email': request.data['email']},  # noqa: C901
                        status=status.HTTP_400_BAD_REQUEST  # noqa: C901
                    )  # noqa: C901
            user.email = request.data['email']  # noqa: C901

        if 'first_name' in request.data:  # noqa: C901
            user.first_name = request.data['first_name']  # noqa: C901
        if 'last_name' in request.data:  # noqa: C901
            user.last_name = request.data['last_name']  # noqa: C901
        if 'bio' in request.data:  # noqa: C901
            user.bio = request.data['bio']  # noqa: C901

        user.save()  # noqa: C901

        return Response(  # noqa: C901
            {  # noqa: C901
                'username': user.username,  # noqa: C901
                'email': user.email,  # noqa: C901
                'first_name': user.first_name,  # noqa: C901
                'last_name': user.last_name,  # noqa: C901
                'bio': user.bio,  # noqa: C901
                'role': user.role,  # noqa: C901
            }  # noqa: C901
        )  # noqa: C901


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_confirmation_code(request):
    user_name = request.data['username']
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

        if serializer.is_valid():
            user = serializer.save()
            code = create_code(user)
            send_email_with_confirmation_code(code, user.email)
            user.confirmation_code = code
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsRoleAdmin]
        elif self.action == 'create':
            permission_classes = [IsRoleAdminOrSuperUser]
        elif self.action == 'retrieve':
            permission_classes = [IsRoleAdmin]
        elif self.action == 'update':
            permission_classes = [IsRoleAdmin]
        elif self.action == 'partial_update':
            permission_classes = [IsRoleAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsRoleAdminOrSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class YamdbTokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
