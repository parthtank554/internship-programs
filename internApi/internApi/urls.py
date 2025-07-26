from django.contrib import admin
from django.urls import path
from API import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('stuinfo/<int:pk>/', views.student_detail),  # URL for student detail view with primary key
    path('stuinfo/', views.student_list),  # URL for student detail view
]
