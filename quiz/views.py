from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Question, StudentResult
from django.contrib import messages


def enter_exam(request):
    if request.method == "POST":
        name = request.POST.get('name')
        index = request.POST.get('index')
        course_code = request.POST.get('course_code')
        exam = Exam.objects.filter(course_code=course_code).first()

        if exam and exam.is_currently_active:
            request.session['student_name'] = name
            request.session['index_number'] = index
            request.session['course_code'] = course_code
            return redirect('take_exam')
        else:
            return render(request, 'entry.html', {'error': "Exam inactive or invalid code."})
    return render(request, 'entry.html')


def take_exam(request):
    code = request.session.get('course_code')
    exam = Exam.objects.filter(course_code=code).first()
    if not exam or not exam.is_currently_active:
        return redirect('enter_exam')
    questions = Question.objects.filter(exam=exam)
    return render(request, 'exam.html', {'exam': exam, 'questions': questions})


def submit_exam(request):
    if request.method == "POST":
        code = request.session.get('course_code')
        name = request.session.get('student_name')
        index = request.session.get('index_number')
        cheat_count = request.POST.get('cheat_count', 0)

        if not code or not name:
            return redirect('enter_exam')

        exam = get_object_or_404(Exam, course_code=code)
        questions = Question.objects.filter(exam=exam)

        # Calculate score
        score = 0
        for q in questions:
            ans = request.POST.get(f'q_{q.id}')
            if str(ans) == str(q.correct_option):
                score += 1

        # Save Result
        StudentResult.objects.create(
            name=name,
            index_number=index,
            course_code=code,
            score=score,
            total_questions=questions.count(),
            cheat_count=cheat_count
        )

        # Clear session to prevent re-entry, but keep data for the score page rendering
        request.session.flush()

        return render(request, 'score.html', {
            'name': name,
            'score': score,
            'total': questions.count(),
            'course': code
        })
    return redirect('enter_exam')