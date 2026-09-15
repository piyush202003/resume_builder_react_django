import json

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from httpx import delete
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


from .gemini_summariser import ai_job_description, ai_professional_summary, ai_upload_resume

from .imagekit_client import upload_resume_image

from .models import Education, Experience, PersonalInfo, Project, ResumeData, Skills
from .serializers import EducationSerializer, ExperienceSerializer, PersonalInfoSerializer, ProjectSerializer, ResumeAllDetailsSerializer, ResumeSerializer, SkillSerializer

# Create your views here.
class ResumeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(user=request.user)
        PersonalInfo.objects.create(
            resume=resume
        )
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
        },status=status.HTTP_200_OK)

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
        serializer=ResumeAllDetailsSerializer(resume)
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
        serializer = ResumeAllDetailsSerializer(resume)
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

        return Response(
            {
                'message':'Resume updated',
                'resume': ResumeSerializer(resume).data
            },
            status=status.HTTP_200_OK
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
        print('AI response =', response)
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
            serializer = ResumeAllDetailsSerializer(resume)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            message = error.body[0]["error"]["message"]
            # message = error.body[0].get("error", {}).get("message", "Permission denied")
            # print(error, vars(error.body[0]))
            return Response(
                {'error':message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# api/resume/{resume_id}/personal-info/
class PersonalInfoUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(
                id=resume_id,
                user=request.user
            )
        except ResumeData.DoesNotExist:
            return Response(
                {'error': 'Resume not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            personal_info = resume.personal_info
        except PersonalInfo.DoesNotExist:
            return Response(
                {'error': 'Personal info not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        personal_info_data = request.data.get( 'personalInfo', '{}')

        try:
            personal_info_data = json.loads(personal_info_data)
        except (json.JSONDecodeError, TypeError):
            return Response(
                {'error': 'Invalid personalInfo data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PersonalInfoSerializer(
            instance=personal_info,
            data=personal_info_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        image = request.FILES.get('image')

        if image:
            remove_background = request.data.get( 'removeBackground', 'false' ) == 'true'

            image_url = upload_resume_image( image, resume.id, remove_background)
            personal_info.image = image_url
            personal_info.save(update_fields=['image'])

        # Re-serialize because image may have changed
        serializer = PersonalInfoSerializer(personal_info)

        return Response(
            {
                'personal_info': serializer.data,
                'message': 'Personal Info has been updated'
            },
            status=status.HTTP_200_OK
        )

class ExperienceAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(id=resume_id, user=request.user)
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        experience = serializer.save(resume=resume)
        return Response(
            ExperienceSerializer(experience).data,
            status = status.HTTP_201_CREATED
        )

class ExperienceUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, resume_id, experience_id):
        try:
            experience = Experience.objects.get(
                id=experience_id,
                resume_id=resume_id,
                resume__user=request.user
            )
        except Experience.DoesNotExist:
            return Response(
                {'error':'Experience not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ExperienceDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, resume_id, experience_id):
        try:
            experience=Experience.objects.get(
                id=experience_id,
                resume_id=resume_id,
                resume__user=request.user
            )
        except Experience.DoesNotExist:
            return Response(
                {'error':'Experience not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        experience.delete()
        return Response(
            {'message':'Experience deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )

class ProjectCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, resume_id):
        try:
            resume= ResumeData.objects.get(id=resume_id, user=request.user)
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(resume=resume)
        return Response(
            {
                'project':ProjectSerializer(project),
                'message':'New Project slot is created.'
            },
            status=status.HTTP_201_CREATED
        )

class ProjectUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, resume_id, project_id):
        try:
            project = Project.objects.get(id=project_id, resume_id=resume_id, resume__user=request.user)
        except Project.DoesNotExist:
            return Response(
                {'error':'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class ProjectDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, resume_id, project_id):
        try:
            project = Project.objects.get(
                id=project_id, 
                resume_id=resume_id,
                resume__user=request.user
            )
        except Project.DoesNotExist:
            return Response(
                {'error':'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        project.delete()
        return Response(
            {'message':'Project deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )

class EducationCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, resume_id):
        try:
            resume = ResumeData.objects.get(id=resume_id, user=request.user)
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume did not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EducationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        education = serializer.save(resume=resume)
        return Response(
            {
                'education':EducationSerializer(education),
                'message':'New Education slot has been created.'
            },
            status=status.HTTP_200_OK
        )

class EducationUpdateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, resume_id, education_id):
        try:
            education = Education.objects.get(id=education_id, resume_id=resume_id, resume__user=request.user)
        except Education.DoesNotExist:
            return Response(
                {'error':'Education did not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EducationSerializer(education, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class EducationDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, resume_id, education_id):
        try:
            education = Education.objects.get(id=education_id, resume_id=resume_id, resume__user=request.user)
        except Education.DoesNotExist:
            return Response(
                {'error':'Education slot did not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        education.delete()
        return Response(
            {'message':'Education slot has been deleted.'},
            status=status.HTTP_200_OK
        )

class SkillCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, resume_id):
        try:
            resume =ResumeData.objects.get(
                id=resume_id, user=request.user
            )
        except ResumeData.DoesNotExist:
            return Response(
                {'error':'Resume did not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        skill = serializer.save(resume=resume)
        return Response(
            SkillSerializer(skill).data,
            status=status.HTTP_201_CREATED
        )

class SkillDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, resume_id, skill_id):
        try:
            skill = Skills.objects.get(id=skill_id, resume_id=resume_id, reusme__user=request.user)
        except Skills.DoesNotExist:
            return Response(
                {'error':"Skill not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        skill.delete()
        return Response(
            {'message':'Skill has been deleted.'},
            status=status.HTTP_200_OK
        )