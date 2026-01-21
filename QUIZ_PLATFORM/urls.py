from django.contrib import admin  # Fixes the 'admin' red error
from django.urls import path, include  # Fixes the 'include' red error
from quiz import views  # Imports your logic from the quiz app

urlpatterns = [
    path('admin/', admin.site.urls),

    # Change 'login' to 'enter_exam' to match your template tags
    path('', views.enter_exam, name='enter_exam'),

    path('exam/', views.take_exam, name='take_exam'),
    path('submit/', views.submit_exam, name='submit_exam'),
]