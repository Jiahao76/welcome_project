from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HomeworkSubmissionForm
from .models import HomeworkSubmission

@login_required
def upload_homework(request):
    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('dashboard')
    else:
        form = HomeworkSubmissionForm()
    return render(request, 'submissions/upload.html', {'form': form})
