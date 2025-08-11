from django.urls import path
from . import views
from .views import *

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

# class base functions URLs

# urlpatterns = [
#     # Authentication
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),

#     # Stories
#     path('', StoryListView.as_view(), name='story_list'),
#     path('stories/<int:story_id>/', StoryDetailView.as_view(), name='story_detail'),
#     path('upload/', UploadStoryView.as_view(), name='upload_story'),
#     path('stories/<int:story_id>/like/', LikeStoryView.as_view(), name='like_story'),
#     path('stories/<int:story_id>/reply/', ReplyStoryView.as_view(), name='reply_story'),

#     # Profile
#     path('profile/', ProfileView.as_view(), name='profile'),
#     path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
# ]