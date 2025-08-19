from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HomeworkSubmissionForm
from .models import HomeworkSubmission
from .utils import log_to_redshift
from django.contrib.auth.decorators import permission_required


@permission_required('submissions.can_upload_homework', raise_exception=True)
@login_required
def upload_homework(request):
    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()

            # ✅ Log upload to Redshift
            log_to_redshift(request.user.username, submission.file.name)

            return redirect('dashboard')
    else:
        form = HomeworkSubmissionForm()
    return render(request, 'submissions/upload.html', {'form': form})
