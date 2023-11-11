from django.contrib import admin
from .models import JobPost, UserApplication, UserAttachment

class UserAttachmentInline(admin.TabularInline):
    model = UserAttachment

class UserApplicationInline(admin.TabularInline):
    model = UserApplication

class UserApplicationAdmin(admin.ModelAdmin):
    inlines = [UserAttachmentInline]

class JobPostAdmin(admin.ModelAdmin):
    inlines = [UserApplicationInline]

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(UserApplication, UserApplicationAdmin)
admin.site.register(UserAttachment)