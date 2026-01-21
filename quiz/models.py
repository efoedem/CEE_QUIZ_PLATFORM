from django.db import models
from django.utils import timezone

class Exam(models.Model):
    TYPE_CHOICES = [
        ('QUIZ', 'Quiz'),
        ('MID_SEM', 'Mid Semester'),
        ('EXAMS', 'Final Exams'),
    ]
    course_code = models.CharField(max_length=20, unique=True)
    exam_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXAMS')
    duration_minutes = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    active_until = models.DateTimeField(null=True, blank=True, help_text="Set the time when this exam should automatically stop.")

    class Meta:
        verbose_name = "Course & Exam Setting"
        verbose_name_plural = "Course Management"

    @property
    def is_currently_active(self):
        if not self.is_active: return False
        if self.active_until and timezone.now() > self.active_until: return False
        return True

    def __str__(self):
        return f"{self.course_code} ({self.get_exam_type_display()})"

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(help_text="Enter 1, 2, 3, or 4")

class StudentResult(models.Model):
    name = models.CharField(max_length=100)
    index_number = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    cheat_count = models.IntegerField(default=0) # NEW FIELD
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course_code} (Cheats: {self.cheat_count})"