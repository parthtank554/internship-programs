from django.contrib import admin
from django.urls import path
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stuapi/', views.student_api),
]
