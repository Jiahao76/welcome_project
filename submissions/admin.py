from django.contrib import admin
from .models import HomeworkSubmission

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username',)
