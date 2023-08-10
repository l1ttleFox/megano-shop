import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authapp.models import Profile, Avatar
from authapp.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class SignInView(APIView):
    """CBV авторизации пользователя."""

    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        data = json.loads(serialized_data)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """CBV регистрации пользователя."""

    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        data = json.loads(serialized_data)
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")

        # try:
        user = User.objects.create_user(username=username, password=password, email="")
        avatar = Avatar.objects.create()
        Profile.objects.create(user=user, fullname=name, avatar=avatar)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

    # except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url="/api/sign-in/")
def sign_out(request):
    """View выхода пользователя."""

    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(UpdateModelMixin, GenericAPIView):
    """View профиля пользователя."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        profile = Profile.objects.get(user__username=self.request.user.username)
        return profile

    def get(self, request):
        profile = Profile.objects.get(user__username=request.user.username)
        return Response(ProfileSerializer(profile).data)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProfilePasswordView(APIView):
    """View обновления пароля пользователя."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = json.loads(json.dumps(request.data))
        old_password = data.get("currentPassword")
        new_password = data.get("newPassword")

        user = User.objects.get(username=request.user.username)
        if user.check_password(old_password):
            user.set_password(new_password)
            return Response(status.HTTP_200_OK)

        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


class AvatarUpdateView(APIView):
    """View обновления аватара пользователя."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            avatar = request.FILES["avatar"]
            request.user.profile.avatar.src = avatar
            if avatar.name:
                request.user.profile.avatar.alt = avatar.name
            return Response(status.HTTP_200_OK)

        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
