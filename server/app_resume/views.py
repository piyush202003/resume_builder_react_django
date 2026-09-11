from os import error

from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .gemini_summariser import ai_job_description, ai_professional_summary

from .imagekit_client import upload_resume_image

from .models import ResumeData
from .serializers import PublicResumeSerializer, ResumeSerializer

# Create your views here.
class ResumeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(user=request.user)
        return Response({
            'message': 'Resume created successfully',
            'resume': ResumeSerializer(resume).data,
        }, status=status.HTTP_201_CREATED)

class ResumeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(id=resume_id, user=request.user)
        except ResumeData.DoesNotExist:
            return Response({
                'error': 'Resume not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        resume.delete()
        return Response({
            'message':'Resume deleted successfully.'
        },status=status.HTTP_204_NO_CONTENT)

class ResumeDetailsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(user=request.user, id=resume_id)
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer=ResumeSerializer(resume)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ResumePublicDetailsAPIView(APIView):
    def get(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(id=resume_id, public=True)
        except ResumeData.DoesNotExist:
            return Response(
                {"error":"Public resume not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PublicResumeSerializer(resume)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ResumeUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(id=resume_id, user=request.user)
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume, data=request.data['resumeData'], partial=True)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()

        image = request.FILES.get('image')
        if image:
            image_url = upload_resume_image(image, resume.id, request.data['removeBackground'])
            personal_info = resume.personal_info
            personal_info.image = image_url
            personal_info.save()

        return Response(
            ResumeSerializer(resume).data,
            status=status.HTTP_200_OKs
        )

class EnhanceProfessionalSummaryAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user_content = request.data.get("userContent")

        if not user_content:
            return Response(
                {"error": "Content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response=ai_professional_summary(user_content)
        except Exception:
            print(Exception.values())
            return Response(
                {'error':str(Exception)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'enhancedContent':response},
            status=status.HTTP_200_OK
        )

class EnhanceJobDescriptionAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user_content = request.data.get('userContent')
        if not user_content:
            return Response(
                {'message':'Content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            response = ai_job_description(user_content)
        except Exception as error:
            return Response(
                {'error':str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'enhancedContent':response},
            status=status.HTTP_200_OK
        )

class UploadResumeAPIView(APIView):
    permission_classes=[IsAuthenticated]
    