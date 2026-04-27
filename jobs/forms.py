from django import forms
from django.contrib.auth.models import User
from .models import Application, UserProfile, Job  

# 1. Application Form 
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL', 'autocomplete': 'off'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

# 2. Professional Signup Form 
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'off'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'autocomplete': 'off'}))
    
    SECURITY_QUESTIONS = [
        ('What is your first pet name?', 'What is your first pet name?'),
        ('What is your mother name?', 'What is your mother name?'),
        ('What was the name of your first school?', 'What was the name of your first school?'),
        ('What is your favorite food?', 'What is your favorite food?'),
    ]

    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control','autocomplete': 'off'}))
    security_question = forms.ChoiceField(choices=SECURITY_QUESTIONS, widget=forms.Select(attrs={'class': 'form-control','autocomplete': 'off'}))
    security_answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Answer','autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address','autocomplete': 'off'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("confirm_password")
        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match")

# 3. Recruiter Job Post Form 
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'salary', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title (e.g. Python Dev)','autocomplete': 'off'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name','autocomplete': 'off'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (e.g. Remote/Delhi)','autocomplete': 'off'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary Package','autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Job Details...','autocomplete': 'off'}),
        }

        