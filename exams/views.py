from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Student, Question, StudentAnswer, ExamResult
from django.contrib import messages
import random
from datetime import datetime


# -----------------------------
# LOGIN VIEW
# -----------------------------
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(username=username, password=password)

            request.session["student_id"] = student.id
            request.session["domain"] = student.domain
            request.session["username"] = student.username

            return redirect("dashboard")

        except Student.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard_view(request):

    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = Student.objects.get(id=student_id)
    
    # CHECK IF QUESTIONS EXIST FOR THIS DOMAIN
    domain = student.domain
    questions_exist = Question.objects.filter(domain=domain).exists()
    
    # CHECK IF EXAM ALREADY ATTEMPTED
    attempted = ExamResult.objects.filter(student=student).exists()

    return render(request, "dashboard.html", {
        "student": student,
        "attempted": attempted,
        "questions_exist": questions_exist,
    })


# -----------------------------
# EXAM INSTRUCTIONS
# -----------------------------
def exam_instructions_view(request):

    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = Student.objects.get(id=student_id)
    
    # CHECK IF QUESTIONS EXIST BEFORE SHOWING INSTRUCTIONS
    domain = student.domain
    questions_exist = Question.objects.filter(domain=domain).exists()
    
    if not questions_exist:
        messages.error(request, "Exams not available for your domain yet. Please contact administrator.")
        return redirect("dashboard")

    return render(request, "exam_instructions.html", {
        "student": student,
        "attempted": ExamResult.objects.filter(student=student).exists()
    })


# -----------------------------
# START EXAM
# -----------------------------
def start_exam_view(request):

    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = Student.objects.get(id=student_id)
    domain = request.session.get("domain")

    # CHECK IF STUDENT ALREADY COMPLETED THE EXAM
    if ExamResult.objects.filter(student=student).exists():
        messages.error(request, "You have already completed this exam!")
        return redirect("dashboard")

    questions = list(Question.objects.filter(domain=domain))

    # CHECK IF QUESTIONS EXIST
    if not questions:
        messages.error(request, "Exams not available for your domain yet. Please contact administrator.")
        return redirect("dashboard")

    random.shuffle(questions)

    # STORE START TIME IN SESSION
    request.session["exam_start_time"] = timezone.now().isoformat()
    request.session["question_order"] = [q.id for q in questions]
    
    # CLEAR ANY PREVIOUS TEMPORARY ANSWERS
    request.session["temp_answers"] = {}

    return render(request, "start_exam.html", {
        "questions": questions,
        "total_questions": len(questions),
        "exam_duration": 60
    })


# -----------------------------
# SUBMIT EXAM
# -----------------------------
def submit_exam_view(request):

    if request.method != "POST":
        return redirect("dashboard")

    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    student = Student.objects.get(id=student_id)

    # CHECK IF ALREADY SUBMITTED
    if ExamResult.objects.filter(student=student).exists():
        messages.error(request, "Exam already submitted!")
        return redirect("dashboard")

    question_order = request.session.get("question_order")
    if not question_order:
        messages.error(request, "No exam session found!")
        return redirect("dashboard")

    questions = list(Question.objects.filter(id__in=question_order))
    
    if not questions:
        messages.error(request, "No questions found!")
        return redirect("dashboard")

    # CLEAR OLD ANSWERS
    StudentAnswer.objects.filter(student=student).delete()

    correct = 0
    wrong = 0
    unanswered = 0

    print("=" * 60)
    print("EXAM SUBMISSION DEBUG")
    print("=" * 60)
    print(f"Student: {student.username}")
    print(f"Total Questions: {len(questions)}")
    print("-" * 60)

    # PROCESS EACH QUESTION
    for question in questions:
        post_key = f"question_{question.id}"
        selected = request.POST.get(post_key, "")
        
        print(f"Q{question.id}: '{selected}' | Correct: '{question.correct_answer}'")

        if not selected or selected == "":
            unanswered += 1
            is_correct = False
            selected_option = None
        elif selected.upper() == question.correct_answer.upper():
            correct += 1
            is_correct = True
            selected_option = selected.upper()
        else:
            wrong += 1
            is_correct = False
            selected_option = selected.upper()

        StudentAnswer.objects.create(
            student=student,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct
        )

    total_questions = len(questions)
    
    if total_questions > 0:
        score = (correct / total_questions) * 100
        score = round(score, 2)
    else:
        score = 0

    print("-" * 60)
    print(f"✅ Correct: {correct}")
    print(f"❌ Wrong: {wrong}")
    print(f"❓ Unanswered: {unanswered}")
    print(f"🎯 Score: {score}%")
    print("=" * 60)

    # Create ExamResult
    ExamResult.objects.create(
        student=student,
        total_questions=total_questions,
        correct_answers=correct,
        wrong_answers=wrong,
        unanswered_answers=unanswered,
        score=score
    )

    # CLEAR EXAM SESSION DATA
    request.session.pop("question_order", None)
    request.session.pop("exam_start_time", None)
    request.session.pop("temp_answers", None)

    messages.success(request, f"Exam submitted successfully! Your score: {score}% ({correct} out of {total_questions})")
    return redirect("result")


# -----------------------------
# RESULT PAGE
# -----------------------------
def result_view(request):

    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("login")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect("login")

    result = ExamResult.objects.filter(student=student).order_by("-id").first()

    if not result:
        return render(request, "result.html", {
            "total_questions": 0,
            "correct": 0,
            "wrong": 0,
            "unanswered": 0,
            "score": 0,
            "results": [],
            "result": None,
            "student": student
        })

    answers = StudentAnswer.objects.filter(student=student).select_related("question")

    results = []

    for ans in answers:
        selected = ans.selected_option

        if not selected or selected == "":
            status = "unanswered"
        elif selected.upper() == ans.question.correct_answer.upper():
            status = "correct"
        else:
            status = "wrong"

        results.append({
            "question": ans.question,
            "selected_option": selected,
            "status": status
        })

    return render(request, "result.html", {
        "result": result,
        "results": results,
        "total_questions": result.total_questions,
        "correct": result.correct_answers,
        "wrong": result.wrong_answers,
        "unanswered": result.unanswered_answers,
        "score": result.score,
        "student": student
    })


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    request.session.flush()
    return redirect("login")


# -----------------------------
# 404 PAGE
# -----------------------------
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)