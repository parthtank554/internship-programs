from django.contrib import admin
from django.urls import path
from API2 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('studcreate/', views.student_create),
]
