from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResumeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, default='Untitled Resume')
    public = models.BooleanField(default=False)
    template = models.CharField(max_length=15, default='classic')
    accent_color = models.CharField(max_length=7, default='#3B82F6')
    professional_summary = models.TextField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return self.title

class Skills(models.Model):
    """Model definition for Skills."""
    resume = models.ForeignKey(ResumeData, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        """Meta definition for Skills."""
        verbose_name = 'Skills'
        verbose_name_plural = 'Skillss'

    def __str__(self):
        """Unicode representation of Skills."""
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # to updated time in ResumeData after making changes in this tables 
        self.resume.save(update_fields=["updated_at"])

def resume_image_path(instance, filename):
    return f"resume_images/{instance.resume.id}_{filename}"
class PersonalInfo(models.Model):
    """Model definition for PersonalInfo."""
    resume = models.OneToOneField( ResumeData, on_delete=models.CASCADE, related_name='personal_info' )
    image = models.FileField( upload_to=resume_image_path, blank=True, null=True )
    full_name = models.CharField( max_length=30, blank=True )
    profession = models.CharField( max_length=30, blank=True )
    email = models.EmailField( blank=True )
    phone = models.CharField( max_length=20, blank=True )
    location = models.CharField( max_length=50, blank=True )
    linkedin = models.URLField( blank=True )
    website = models.URLField( blank=True )

    class Meta:
        """Meta definition for PersonalInfo."""
        verbose_name = 'PersonalInfo'
        verbose_name_plural = 'PersonalInfos'

    def __str__(self):
        """Unicode representation of PersonalInfo."""
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # to updated time in ResumeData after making changes in this tables 
        self.resume.save(update_fields=["updated_at"])

class Experience(models.Model):
    """Model definition for Experience."""
    resume = models.ForeignKey(ResumeData, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField( max_length=150, blank=True )
    position = models.CharField( max_length=150, blank=True)
    start_date = models.DateField( blank=True)
    end_date = models.DateField( blank=True, null=True )
    description = models.TextField( max_length=2000, blank=True)
    is_current = models.BooleanField( default=False )
    class Meta:
        """Meta definition for Experience."""

        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        """Unicode representation of Experience."""
        return self.company

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # to updated time in ResumeData after making changes in this tables 
        self.resume.save(update_fields=["updated_at"])

class Project(models.Model):
    """Model definition for Project."""
    resume = models.ForeignKey(ResumeData, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField( max_length=150, blank=True)
    type = models.CharField( max_length=150, blank=True)
    description = models.TextField( max_length=2000, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # to updated time in ResumeData after making changes in this tables 
        self.resume.save(update_fields=["updated_at"])

class Education(models.Model):
    """Model definition for Education."""
    resume = models.ForeignKey(ResumeData, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField( max_length=200, blank=True)
    degree = models.CharField( max_length=100, blank=True)
    field = models.CharField( max_length=100, blank=True)
    granduation_date = models.DateField( blank=True, null=True)
    gpa = models.CharField( max_length=10, blank=True)
    
    class Meta:
        """Meta definition for Education."""

        verbose_name = 'Education'
        verbose_name_plural = 'Educations'

    def __str__(self):
        """Unicode representation of Education."""
        return self.degree

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # to updated time in ResumeData after making changes in this tables 
        self.resume.save(update_fields=["updated_at"])