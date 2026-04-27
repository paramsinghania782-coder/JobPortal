from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, UserProfile, Application
from .forms import ApplicationForm, UserSignupForm, JobForm
from django.core.paginator import Paginator
from django.http import JsonResponse

# 1. Home Page (Search Logic)
def home(request):
    query = request.GET.get('q')
    if query:
        jobs_list = Job.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-created_at')  
    else:
        jobs_list = Job.objects.all().order_by('-created_at')

    
    paginator = Paginator(jobs_list, 21)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/home.html', {'jobs': jobs, 'query': query})

# 2. Job Detail & Application Logic
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.is_authenticated:
        initial_data = {
            'full_name': request.user.username,
            'email': request.user.email
        }
    else:
        initial_data = {}

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return render(request, 'jobs/success.html', {'job': job})
    else:
        form = ApplicationForm(initial=initial_data)

    return render(request, 'jobs/job_detail.html', {'job': job, 'form': form})

# 3. Signup Logic
def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                security_question=form.cleaned_data['security_question'],
                security_answer=form.cleaned_data['security_answer']
            )
            messages.success(request, "Account created! Please login.")
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# 4. Login Logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_input = request.POST.get('password')
        role_selected = request.POST.get('login_role')

        user = authenticate(request, username=username, password=pass_input)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == role_selected:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, f"Access Denied: You are registered as a {profile.role}, not a {role_selected}.")
            except UserProfile.DoesNotExist:
                 messages.error(request, "Error: User profile not found.")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'registration/login.html')

# --- RECRUITER FEATURES ---

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    total_candidates = Application.objects.filter(job__recruiter=request.user).count()

    context = {
        'jobs': jobs,
        'total_candidates': total_candidates  
    }
    return render(request, 'jobs/recruiter_dashboard.html', context)

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()

            return render(request, 'jobs/job_post_success.html') 

    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job Updated!")
            return redirect('recruiter_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/post_job.html', {'form': form, 'title': 'Edit Job'})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    job.delete()
    messages.success(request, "Job Deleted Successfully")
    return redirect('recruiter_dashboard')

@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    applicants = job.application_set.all()
    return render(request, 'jobs/applicants.html', {'job': job, 'applicants': applicants})

# --- CANDIDATE FEATURES ---

@login_required
def candidate_dashboard(request):
    my_apps = Application.objects.filter(email=request.user.email).order_by('-applied_at')
    return render(request, 'jobs/candidate_dashboard.html', {'apps': my_apps})

@login_required
def delete_application(request, app_id):
    app = get_object_or_404(Application, pk=app_id, email=request.user.email)
    app.delete()
    messages.success(request, "Application Withdrawn Successfully.")
    return redirect('candidate_dashboard')

@login_required
def edit_application(request, app_id):
    app = get_object_or_404(Application, pk=app_id, email=request.user.email)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume Updated Successfully!")
            return redirect('candidate_dashboard')
    else:
        form = ApplicationForm(instance=app)
    return render(request, 'jobs/edit_application.html', {'form': form, 'app': app})

# --- SMART REDIRECT ---

@login_required
def after_login_redirect(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    elif hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'recruiter':
        return redirect('recruiter_dashboard')

    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        answer = request.POST.get('security_answer')
        new_password = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            
            if profile.security_answer.lower() == answer.lower():
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful! Please login.")
                return redirect('login')
            else:
                messages.error(request, "Wrong security answer!")
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "Username not found!")
            
    return render(request, 'registration/forgot_password.html')

def get_security_question(request):
    username = request.GET.get('username', None)
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        return JsonResponse({'question': profile.security_question})
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return JsonResponse({'error': 'Username not found'}, status=404)


def about_us(request):
    return render(request, 'jobs/about.html')

def contact_us(request):
    return render(request, 'jobs/contact.html')

def terms(request):
    return render(request, 'jobs/terms.html')

def privacy(request):
    return render(request, 'jobs/privacy.html')