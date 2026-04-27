from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Job, Application

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)  
    list_display = ('username', 'email', 'get_user_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    def get_user_role(self, obj):
        
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.role 
        return '-'
    
    get_user_role.short_description = 'Role'  

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Application)