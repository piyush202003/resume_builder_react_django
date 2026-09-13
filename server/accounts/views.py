from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from app_resume.models import ResumeData

from .serializers import LoginSerializer, RegisterSerializer, UserResumesInfoSerializer, UserSerializer

from django.contrib.auth.models import User


# Create your views here.
class LoginApiView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user' : {
                'id' :user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message':'Resitration successful',
            'user':{
                'id':user.id,
                'username':user.username,
                'email':user.email,
            }
        },status=status.HTTP_201_CREATED)

class UserDataApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        serializer = UserSerializer(user)
        return Response({
            'message':'Got User Details',
            'user':serializer.data
        }, status=status.HTTP_302_FOUND)

class UserResumesApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        resumes = ResumeData.objects.filter(user=request.user)
        serializer = UserResumesInfoSerializer(resumes)
        return Response({
            'message': 'Got all your Resumes',
            'resumes': serializer.data,
        }, status=status.HTTP_200_OK)