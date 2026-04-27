from django.db import models
from django.contrib.auth.models import User  # User import karna zaroori hai

# 1. Job Model
class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs') # <-- New Field
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50)
    salary = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 2. Application Model
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} applied for {self.job.title}"

# 3. User Profile 
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    security_question = models.CharField(max_length=200)
    security_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} - {self.role}"