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
        read_only_fileds = [ 'id', 'resume' ]

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fileds = [ 'id', 'resume' ]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fileds = [ 'id', 'resume' ]

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fileds = [ 'id', 'resume' ]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = [ 'id', 'type' ]
        read_only_fileds = [ 'id', 'resume' ]

class ResumeAllDetailsSerializer(serializers.ModelSerializer):
    personal_info = PerosnalInfoSerializer(read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    project = ProjectSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeData
        fields = [ 'id', 'title', 'template', 'accent_color', 'public', 'professional_summary', 'updated_at', 'personal_info', 'experience', 'project', 'education', 'skills']
        read_only_fileds = [ 'id' ]