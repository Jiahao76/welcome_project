from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from submissions.models import HomeworkSubmission
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from submissions.models import HomeworkSubmission

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def generate_presigned_url(s3_key):
    s3_client = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=300  # 5 minutes
        )
    except ClientError:
        url = None
    return url


@login_required
def dashboard_view(request):
    submissions = HomeworkSubmission.objects.filter(user=request.user)
    for item in submissions:
        item.presigned_url = generate_presigned_url(item.file.name)
    return render(request, 'accounts/dashboard.html', {'submissions': submissions})
