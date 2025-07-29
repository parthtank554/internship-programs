from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.create_user, name='create_user'),
    path('edit/<int:id>/', views.student_edit, name='student_update'),
    path('delete/<int:id>/', views.student_delete, name='student_delete'),
]