from django.db import models


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)

    DOMAIN_CHOICES = [
        ("PHP Full Stack Web Development", "PHP Full Stack Web Development"),
        ("Python Full Stack Web Development", "Python Full Stack Web Development"),
        ("Java Full Stack Web Development", "Java Full Stack Web Development"),
        ("MERN Stack Development", "MERN Stack Development"),
        ("MEAN Stack Development", "MEAN Stack Development"),
        ("Data Analytics", "Data Analytics"),
        ("Cloud Computing", "Cloud Computing"),
        ("Artificial Intelligence / Machine Learning", "Artificial Intelligence / Machine Learning"),
    ]

    domain = models.CharField(max_length=200, choices=DOMAIN_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# -----------------------------
# Question Model
# -----------------------------
class Question(models.Model):

    DOMAIN_CHOICES = [
        ("PHP Full Stack Web Development", "PHP Full Stack Web Development"),
        ("Python Full Stack Web Development", "Python Full Stack Web Development"),
        ("Java Full Stack Web Development", "Java Full Stack Web Development"),
        ("MERN Stack Development", "MERN Stack Development"),
        ("MEAN Stack Development", "MEAN Stack Development"),
        ("Data Analytics", "Data Analytics"),
        ("Cloud Computing", "Cloud Computing"),
        ("Artificial Intelligence / Machine Learning", "Artificial Intelligence / Machine Learning"),
    ]

    domain = models.CharField(max_length=200, choices=DOMAIN_CHOICES)

    question_text = models.TextField()

    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50]


# -----------------------------
# Student Answer Model
# -----------------------------
class StudentAnswer(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_option = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ],
        blank=True,
        null=True
    )

    # True = correct, False = wrong, None = unanswered
    is_correct = models.BooleanField(null=True, blank=True)

    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - Q{self.question.id}"


# -----------------------------
# Exam Result Model
# -----------------------------
class ExamResult(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    total_questions = models.IntegerField()

    correct_answers = models.IntegerField()

    wrong_answers = models.IntegerField()
    
    unanswered_answers = models.IntegerField(default=0)  # FIXED: Added this field

    score = models.FloatField()  # FIXED: Changed from IntegerField to FloatField for percentage

    exam_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - Score {self.score}"


# -----------------------------
# Excel Upload Model (Admin Upload)
# -----------------------------
class QuestionUpload(models.Model):

    excel_file = models.FileField(upload_to="question_excel/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel Upload {self.id}"