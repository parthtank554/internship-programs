from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Story URLs
    path('', views.story_list, name='story_list'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    # path('story/<int:story_id>/unlike/', views.unlike_story, name='unlike_story'),
    path('upload/', views.upload_story, name='upload_story'),
    path('story/<int:story_id>/like/', views.like_story, name='like_story'),
    path('story/<int:story_id>/reply/', views.reply_story, name='reply_story'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # Add this to urlpatterns
    # path('debug-db/', views.debug_db, name='debug_db'),
]