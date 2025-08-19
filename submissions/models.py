from django.db import models
from django.contrib.auth.models import User

class HomeworkSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
    
    class Meta:
        permissions = [
            ("can_upload_homework", "Can upload homework"),
        ]
