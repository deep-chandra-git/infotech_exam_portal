from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student, Question, StudentAnswer, ExamResult


# -----------------------------
# Student Admin
# -----------------------------
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "full_name",
        "domain",
        "created_at"
    )

    search_fields = (
        "username",
        "full_name",
        "domain"
    )

    list_filter = (
        "domain",
        "created_at"
    )


# -----------------------------
# Question Admin
# Excel Upload Enabled
# -----------------------------
class QuestionAdmin(ImportExportModelAdmin):

    list_display = (
        "id",
        "domain",
        "question_text",
        "correct_answer",
        "created_at"
    )

    search_fields = (
        "question_text",
        "domain"
    )

    list_filter = (
        "domain",
        "created_at"
    )


# -----------------------------
# Student Answer Admin
# -----------------------------
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "question",
        "selected_option",
        "is_correct",
        "answered_at"
    )

    search_fields = (
        "student__username",
        "question__question_text"
    )

    list_filter = (
        "is_correct",
        "answered_at"
    )


# -----------------------------
# Exam Result Admin
# -----------------------------
class ExamResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "total_questions",
        "correct_answers",
        "wrong_answers",
        "score",
        "exam_date"
    )

    search_fields = (
        "student__username",
    )

    list_filter = (
        "exam_date",
    )


# -----------------------------
# Register Models
# -----------------------------
admin.site.register(Student, StudentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(ExamResult, ExamResultAdmin)