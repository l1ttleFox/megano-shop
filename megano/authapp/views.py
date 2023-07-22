import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authapp.models import Profile


class SignInView(APIView):
    """ CBV для авторизации пользователя. """
    
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        data = json.loads(serialized_data)
        name = data.gert("name")
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class SignUpView(APIView):
    """ CBV для регистрации пользователя. """
    
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        data = json.loads(serialized_data)
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
    
        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullname=name)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
def sign_out(request):
    """ View для выхода пользователя. """
    
    logout(request)
    return Response(status=status.HTTP_200_OK)