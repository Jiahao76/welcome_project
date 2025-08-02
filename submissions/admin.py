import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.contrib import admin
from .models import HomeworkSubmission

@admin.action(description="Download selected homeworks")
def download_selected_homeworks(modeladmin, request, queryset):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for submission in queryset:
            file_field = submission.file
            if file_field:
                file_name = file_field.name.split('/')[-1]
                file_content = file_field.read()
                zip_file.writestr(file_name, file_content)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="homeworks.zip"'
    return response

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username',)
    actions = [download_selected_homeworks]
