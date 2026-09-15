from django.urls import path
from .views import *

# api/resume/
urlpatterns = [
    path('create/', ResumeCreateAPIView.as_view(), name='resume_create'),
    path('delete/<int:resume_id>/',ResumeDeleteAPIView.as_view(), name='resume_delete'),
    path('details/<int:resume_id>/', ResumeDetailsAPIView.as_view(), name='resume_details'),
    path('public/<int:resume_id>/', ResumePublicDetailsAPIView.as_view(), name='public_resume_details'),
    path('update/<int:resume_id>/', ResumeUpdateAPIView.as_view(), name='resume_update'), 
    path('ai/enchance-pro-sum/', EnhanceProfessionalSummaryAPIView.as_view(), name='ai_professional_summary'),
    path('ai/enhance-job-desc/', EnhanceJobDescriptionAPIView.as_view(), name='ai_job_description'),
    path('upload/', UploadResumeAPIView.as_view(), name='upload_resume'),

    path('update/<int:resume_id>/personal-info/', PersonalInfoUpdateAPIView.as_view(), name='personal_info_update'),

    path('<int:resume_id>/experiences/', ExperienceAPIView.as_view(), name='experience-create'),
    path('<int:resume_id>/experiences/<int:experience_id>/', ExperienceUpdateAPIView.as_view(), name='experience-update'),
    path('<int:resume_id>/experiences/<int:experience_id>/delete/', ExperienceDeleteAPIView.as_view(), name='experience-delete'),

    path('<int:resume_id>/projects/', ProjectCreateAPIView.as_view(), name='project-create'),
    path('<int:resume_id>/projects/<int:project_id>/', ProjectUpdateAPIView.as_view(), name='project-update'),
    path('<int:resume_id>/projects/<int:project_id>/delete/', ProjectDeleteAPIView.as_view(), name='project-delete'),

    path('<int:resume_id>/educations/', EducationCreateAPIView.as_view(), name='education-create'),
    path('<int:resume_id>/educations/<int:education_id>/', EducationUpdateAPIView.as_view(), name='education-update'),
    path('<int:resume_id>/educations/<int:education_id>/delete/', EducationDeleteAPIView.as_view(), name='education-delete'),

    path('<int:resume_id>/skills/', SkillCreateAPIView.as_view(), name='skill-create'),
    path('<int:resume_id>/skills/<int:skill_id>/delete/', SkillDeleteAPIView.as_view(), name='skill-delete'),
]  