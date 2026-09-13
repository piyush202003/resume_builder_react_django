from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from app_resume.models import ResumeData

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        User = get_user_model()
        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Account with this email does not exists.')
        
        user = authenticate(username=user_obj.get_username(), password=password)

        if not user: 
            raise serializers.ValidationError('Wrong password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive')

        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [ 'id', 'username', 'email', 'password' ]
        read_only_fileds = [ 'id' ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ 'id', 'username', 'email', ]

class UserResumesInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumeData
        fields = [ 'title', 'created_at', 'updated_at' ]