from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('exam-instructions/', views.exam_instructions_view, name='exam_instructions'),
    path('start-exam/', views.start_exam_view, name='start_exam'),
    path('submit-exam/', views.submit_exam_view, name='submit_exam'),
    path('result/', views.result_view, name='result'),
    path('logout/', views.logout_view, name='logout'),
]