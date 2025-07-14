from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_homework, name='upload_homework'),
]
