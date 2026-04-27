from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from jobs import views

urlpatterns = [
    
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/')),

    # --- 2. MAIN ADMIN URL ---
    path('admin/', admin.site.urls),

    # Smart Redirect URL 
    path('after-login/', views.after_login_redirect, name='after_login_redirect'),

    # --- 3. WEBSITE URLs ---
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),

    # Recruiter URLs
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),

    # Candidate URLs
    path('my-applications/', views.candidate_dashboard, name='candidate_dashboard'),
    path('delete-app/<int:app_id>/', views.delete_application, name='delete_application'),
    path('edit-app/<int:app_id>/', views.edit_application, name='edit_application'),

    path('about/', views.about_us, name='about'),
path('contact/', views.contact_us, name='contact'),
path('terms/', views.terms, name='terms'),
path('privacy/', views.privacy, name='privacy'),
path('forgot-password/', views.forgot_password, name='forgot_password'),
path('get-security-question/', views.get_security_question, name='get_security_question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)