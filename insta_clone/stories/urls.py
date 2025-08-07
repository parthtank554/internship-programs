from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('upload/', views.upload_story, name='upload_story'),
    path('like/<int:story_id>/', views.like_story, name='like_story'),
    path('reply/<int:story_id>/', views.reply_story, name='reply_story'),
]
