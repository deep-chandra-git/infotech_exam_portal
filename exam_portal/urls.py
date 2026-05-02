"""
URL configuration for exam_portal project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Admin Panel
    path('admin/', admin.site.urls),

    # Exams App URLs
    path('', include('exams.urls')),

]

# Custom 404 Page
handler404 = "exams.views.custom_404_view"