from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Education, Experience, PersonalInfo, Project, ResumeData, Skills

class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumeData
        fields = [ 'id', 'title', 'public', 'template', 'accent_color', 'professional_summary', 'created_at', 'updated_at', ]
        read_only_fields = [ 'id', 'created_at', 'updated_at' ]

class PerosnalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = [ 'id', 'type' ]

class PublicResumeSerializer(serializers.ModelSerializer):
    personal_info = PerosnalInfoSerializer(read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeData
        fields = [ 'id', 'title', 'template', 'accent_color', 'professional_summary', 'updated_at', 'personal_info', 'experiences', 'projects', 'educations', 'skills']