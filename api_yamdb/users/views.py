from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializerForCode, UsersSerializer
from .serializers import YamdbTokenSerializer
from .permissions import (
    IsRoleAdminOrOwner,
    IsRoleOwner,
    IsRoleAdmin,
    IsRoleSuperUser,
    IsRoleAdminOrSuperUser
)
from .confirmation_code import send_email_with_confirmation_code, create_code


@api_view(["GET", "PATCH"])
@permission_classes((IsAuthenticated,))
def get_me(request):
    if request.method == "GET":
        user = request.user

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "role": user.role,
            }
        )

    if request.method == "PATCH":
        user = request.user
        if "username" in request.data:
            if user.username != request.data["username"]:
                if not User.objects.filter(
                    username=request.data["username"]
                ) is None:
                    return Response(
                        {"username": request.data["username"]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            user.username = request.data["username"]

        if "email" in request.data:
            if user.email != request.data["email"]:
                if not User.objects.filter(
                    email=request.data["email"]
                ) is None:
                    return Response(
                        {"email": request.data["email"]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            user.email = request.data["email"]

        if "first_name" in request.data:
            user.first_name = request.data["first_name"]
        if "last_name" in request.data:
            user.last_name = request.data["last_name"]
        if "bio" in request.data:
            user.bio = request.data["bio"]

        user.save()

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "role": user.role,
            }
        )


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_confirmation_code(request):
    user_name = request.data["username"]
    e_mail = request.data["email"]
    user = get_object_or_404(User, username=user_name, email=e_mail)
    if user.confirmation_code is None:
        conf_code = create_code(user)
        user.confirmation_code = conf_code
        user.save()
    else:
        conf_code = user.confirmation_code

    send_email_with_confirmation_code(conf_code, user.email)

    return Response(
        {"username": user_name}
    )


"""class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerForCode
    permission_classes = (AllowAny,)"""


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
    queryset = User.objects.all().order_by("username")
    serializer_class = UsersSerializer
    # permission_classes = [IsRoleAdmin | IsRoleSuperUser | IsRoleOwner]
    pagination_class = PageNumberPagination
    lookup_field = "username"

    # @action(detail=False, methods=["get"], permission_classes=[IsRoleAdmin])
    # def list(self, request):
    # print("8888888888**********888888888888888")
    # recent_users = User.objects.all().order_by("username")
    # serializer = self.get_serializer(recent_users, many=True)
    # return Response(serializer.data)

    # @action(detail=True, methods=["get"], permission_classes=[IsRoleAdmin])
    # def get_user(self, request):
    # serializer = self.get_serializer(self.request.user, many=False)
    # return Response(serializer.data)

    # @action(
    # detail=True,
    # methods=["patch"],
    # permission_classes=[IsRoleAdminOrOwner]
    # )
    # def patch_user(self, request):
    # serializer = self.get_serializer(self.request.user, many=False)
    # return Response(serializer.data)

    # @action(
    # detail=True,
    # methods=["delete"],
    # permission_classes=[IsRoleAdmin]
    # )
    # def delete_user(self, request):
    # serializer = self.get_serializer(self.request.user, many=False)
    # return Response(serializer.data)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsRoleAdmin]
        elif self.action == "create":
            permission_classes = [IsRoleAdminOrSuperUser]
            # return [IsRoleAdmin | IsRoleSuperUser]
        elif self.action == "retrieve":
            permission_classes = [IsRoleAdmin]
        elif self.action == "update":
            permission_classes = [IsRoleAdmin]
            # return (IsRoleAdmin(), IsRoleOwner(),)
        elif self.action == "partial_update":
            permission_classes = [IsRoleAdmin]
            # return (IsRoleAdmin(), IsRoleOwner(),)
        elif self.action == "destroy":
            permission_classes = [IsRoleAdminOrSuperUser]
            # return (IsRoleAdmin(), IsRoleSuperUser(),)
        else:
            permission_classes = [IsAuthenticated]
            # return (IsAuthenticated(),)
        return [permission() for permission in permission_classes]


class YamdbTokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data["username"]
            )
            refresh = RefreshToken.for_user(user)
            return Response({"token": str(refresh.access_token)})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YamdbCodeViewSet(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = YamdbTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"username": serializer.username}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
