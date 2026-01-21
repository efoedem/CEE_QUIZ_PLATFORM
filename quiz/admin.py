import pandas as pd
import openpyxl
from django.contrib import admin, messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.http import HttpResponse
from django import forms
from .models import Exam, Question, StudentResult


# --- FORMS ---
class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label="Select Excel File (.xlsx)")


# --- INLINES ---
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


# --- ADMIN CLASSES ---

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'exam_type', 'duration_minutes', 'is_active', 'active_until')
    list_editable = ('is_active',)
    inlines = [QuestionInline]
    change_form_template = "admin/course_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Use <int:> to force Django to only pick the numeric ID
            path('<int:object_id>/upload-questions/', self.admin_site.admin_view(self.upload_excel),
                 name='course-upload-excel'),
            path('download-template/', self.admin_site.admin_view(self.download_template),
                 name='download-template'),
        ]
        # Custom URLs must come BEFORE standard URLs
        return custom_urls + urls

    def download_template(self, request):
        """ Generates the required Excel structure for the user """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Question Template"
        headers = ['question', 'option 1', 'option 2', 'option 3', 'option 4', 'correct index']
        ws.append(headers)
        ws.append(['What is the capital of Ghana?', 'Kumasi', 'Accra', 'Tamale', 'Takoradi', 2])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=exam_question_template.xlsx'
        wb.save(response)
        return response

    def upload_excel(self, request, object_id):
        # Fetch the exam instance using the integer ID
        exam_instance = get_object_or_404(Exam, pk=object_id)

        if request.method == "POST":
            excel_file = request.FILES.get("excel_file")
            try:
                df = pd.read_excel(excel_file)
                df.columns = [str(c).strip().lower() for c in df.columns]
                df = df.dropna(subset=['question'])

                count = 0
                for _, row in df.iterrows():
                    Question.objects.create(
                        exam=exam_instance,
                        text=str(row['question']).strip(),
                        option1=str(row['option 1']).strip(),
                        option2=str(row['option 2']).strip(),
                        option3=str(row['option 3']).strip(),
                        option4=str(row['option 4']).strip(),
                        correct_option=int(row['correct index'])
                    )
                    count += 1

                messages.success(request, f"Successfully uploaded {count} questions to {exam_instance.course_code}")
                return redirect(f"/admin/quiz/exam/{object_id}/change/")

            except Exception as e:
                messages.error(request, f"Upload Failed: {e}. Ensure you used the template headers.")

        form = ExcelImportForm()
        return render(request, "admin/excel_upload.html", {"form": form, "exam": exam_instance})


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'index_number', 'course_code', 'score', 'total_questions', 'submitted_at')
    list_filter = ('course_code', 'submitted_at')
    search_fields = ('name', 'index_number')
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Exam Results"
        headers = ['Full Name', 'Index Number', 'Course Code', 'Score', 'Total Questions', 'Date Submitted']
        ws.append(headers)
        for obj in queryset:
            ws.append([obj.name, obj.index_number, obj.course_code, obj.score, obj.total_questions,
                       obj.submitted_at.replace(tzinfo=None)])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"Results_{queryset[0].course_code}.xlsx" if queryset.exists() else "Results.xlsx"
        response['Content-Disposition'] = f'attachment; filename={filename}'
        wb.save(response)
        return response

    export_to_excel.short_description = "Download Selected Results as Excel"