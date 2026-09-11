from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .gemini_summariser import ai_job_description, ai_professional_summary, ai_upload_resume

from .imagekit_client import upload_resume_image

from .models import Education, Experience, PersonalInfo, Project, ResumeData, Skills
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
        except Exception as error:
            return Response(
                {'error':error.body[0]["error"]["message"]},
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
                {'error':error.body[0]["error"]["message"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'enhancedContent':response},
            status=status.HTTP_200_OK
        )

class UploadResumeAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        resume_text = request.data.get('resumeText')
        title = request.data.get('title')

        if not resume_text:
            return Response(
                {'message':'Missing required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            extracted_data = ai_upload_resume(resume_text)
            with transaction.atomic():
                resume = ResumeData.objects.create(
                    user=request.user,
                    title=title,
                    professional_summary=extracted_data.get('professional_summary', "")
                )
                personal_info_data = extracted_data.get('personal_info', {})
                PersonalInfo.objects.create(
                    resume=resume,
                    full_name=personal_info_data.get('full_name',""),
                    profession=personal_info_data.get('profession',''),
                    email=personal_info_data.get('email', ''),
                    phone=personal_info_data.get('phone', ''),
                    location=personal_info_data.get('location',''),
                    linkedin=personal_info_data.get('linkedin', ''),
                    website=personal_info_data.get('website', '')
                )

                for skill_data in extracted_data.get('skills', []):
                    Skills.objects.create(
                        resume=resume,
                        type=skill_data.get('type', '')
                    )

                for experience_data in extracted_data.get('experiences',[]):
                    Experience.objects.create(
                        resume=resume,
                        company=experience_data.get('company', ''),
                        position=experience_data.get('position', ''),
                        start_date=experience_data.get('start_date'),
                        end_date=experience_data.get('end_date'),
                        description=experience_data.get('description', ''),
                        is_current=experience_data.get('is_current', False)
                    )

                for project_data in extracted_data.get('projects', []):
                    Project.objects.create(
                        resume=resume,
                        name=project_data.get('name',''),
                        project_type=project_data.get('project_type', ''),
                        description=project_data.get('description', ''),
                        github_url=project_data.get('github_url', ''),
                        live_url=project_data.get('live_url', '')
                    )

                for education_data in extracted_data.get('educations', []):
                    Education.objects.create(
                        resume=resume,
                        institution=education_data.get('institution', ''),
                        degree=education_data.get('degree', ''),
                        field=education_data.get('field', ''),
                        start_date=education_data.get('start_date'),
                        graducation_date=education_data.get('graducatoin_date'),
                        gpa=education_data.get('gpa', '')
                    )
            serializer = PublicResumeSerializer(resume)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            message = error.body[0]["error"]["message"]
            # message = error.body[0].get("error", {}).get("message", "Permission denied")
            return Response(
                {'error':message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )