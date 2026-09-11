from django.urls import path
from .views import *

urlpatterns = [
    path('create/', ResumeCreateAPIView.as_view(), name='resume_create'),
    path('delete/<int:resume_id>/',ResumeDeleteAPIView.as_view(), name='resume_delete'),
    path('details/<int:resume_id>/', ResumeDetailsAPIView.as_view(), name='resume_details'),
    path('public/<int:resume_id>/', ResumePublicDetailsAPIView.as_view(), name='public_resume_details'),
    path('update/<int:resume_id>/', ResumeUpdateAPIView.as_view(), name='resume_update'), 
    path('ai/enchance-pro-sum/', EnhanceProfessionalSummaryAPIView.as_view(), name='ai_professional_summary'),
    path('ai/enhance-job-desc/', EnhanceJobDescriptionAPIView.as_view(), name='ai_job_description'),
     
]  