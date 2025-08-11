# Authentication Views
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         full_name = request.POST['full_name']
        
#         # Check if username or email already exists
#         if user_ops.get_user_by_username(username):
#             return render(request, 'registration/register.html', {'error': 'Username already exists'})
        
#         if user_ops.get_user_by_email(email):
#             return render(request, 'registration/register.html', {'error': 'Email already exists'})
        
#         # Register user
#         user_id = user_ops.register_user(username, email, password, full_name)
        
#         # Set session
#         request.session['user_id'] = user_id
#         request.session['username'] = username
        
#         return redirect('story_list')
    
#     return render(request, 'registration/register.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = user_ops.authenticate_user(username, password)
        
#         if user:
#             # Set session
#             request.session['user_id'] = user['id']
#             request.session['username'] = user['username']
            
#             return redirect('story_list')
#         else:
#             return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    
#     return render(request, 'registration/login.html')

# def logout(request):
#     # Clear session
#     request.session.flush()
#     return redirect('login')

# # Story Views
# def story_list(request):
#     stories = story_ops.get_active_stories()
#     return render(request, 'stories/story_list.html', {'stories': stories})

# # views.py
# def story_detail(request, story_id):
#     con = get_db_connection()
#     cursor = con.cursor()
#     # Call procedure to fetch single story with user info
#     cursor.callproc('GETSINGLESTORYBYID', [story_id])

#     story = None
#     for result in cursor.stored_results():
#         row = result.fetchone()
#         if row:
#             story = {
#                 'id': row[0],
#                 'user_id': row[1],
#                 'username': row[2],
#                 'profile_pic': row[3],
#                 'media_url': row[4],
#                 'media_type': row[5],
#                 'duration': row[6],
#                 'created_at': row[7],
#             }
#     con.close()

#     if not story:
#         return HttpResponse("Story not found.", status=404)

#     return render(request, 'stories/story_detail.html', {
#         'story': story,
#         'current_time': timezone.now()  # for time display
#     })

# @login_required_session
# def upload_story(request):
#     if request.method == 'POST':
#         media_type = request.POST['media_type']
#         duration = int(request.POST.get('duration', 30))
        
#         # Save uploaded file
#         uploaded_file = request.FILES['media']
#         fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
#         filename = fs.save(uploaded_file.name, uploaded_file)
#         file_url = fs.url(filename)
        
#         # Create story
#         user_id = request.session.get('user_id')
#         story_ops.create_story(user_id, file_url, media_type, duration)
        
#         return redirect('story_list')
    
#     return render(request, 'stories/upload_story.html')

# @login_required_session
# def like_story(request, story_id):
#     user_id = request.session.get('user_id')
#     story_ops.add_story_like(user_id, story_id)
#     return redirect('story_detail', story_id=story_id)

# @login_required_session
# def reply_story(request, story_id):
#     if request.method == 'POST':
#         message = request.POST['message']
#         user_id = request.session.get('user_id')
#         story_ops.add_story_reply(user_id, story_id, message)
    
#     return redirect('stories/story_detail', story_id=story_id)

# @login_required_session
# def profile(request):
#     user_id = request.session.get('user_id')
#     user = user_ops.get_user_by_id(user_id)
#     stories = story_ops.get_user_stories(user_id)
    
#     return render(request, 'stories/profile.html', {'user': user, 'stories': stories})

# @login_required_session
# def edit_profile(request):
#     user_id = request.session.get('user_id')
#     user = user_ops.get_user_by_id(user_id)
    
#     if request.method == 'POST':
#         full_name = request.POST['full_name']
        
#         profile_pic = user['profile_pic']
#         if 'profile_pic' in request.FILES:
#             uploaded_file = request.FILES['profile_pic']
#             fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
#             filename = fs.save(uploaded_file.name, uploaded_file)
#             profile_pic = fs.url(filename)
        
#         user_ops.update_user_profile(user_id, full_name, profile_pic)
#         return redirect('profile')
    
#     return render(request, 'stories/edit_profile.html', {'user': user})


from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .Operations import user_ops, story_ops
import os
from django.http import HttpResponse, Http404
from django.utils import timezone
from .decorators import login_required_session
from .Operations.story_ops import *
from .Operations import *
from django.views import View
# -------------------- Authentication Views --------------------

class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        full_name = request.POST['full_name']

        if user_ops.get_user_by_username(username):
            return render(request, 'registration/register.html', {'error': 'Username already exists'})

        if user_ops.get_user_by_email(email):
            return render(request, 'registration/register.html', {'error': 'Email already exists'})

        user_id = user_ops.register_user(username, email, password, full_name)

        request.session['user_id'] = user_id
        request.session['username'] = username

        return redirect('story_list')


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = user_ops.authenticate_user(username, password)

        if user:
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            return redirect('story_list')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')

# -------------------- Story Views --------------------

class StoryListView(View):
    def get(self, request):
        stories = story_ops.get_active_stories()
        return render(request, 'stories/story_list.html', {'stories': stories})


class StoryDetailView(View):
    def get(self, request, story_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.callproc('GETSINGLESTORYBYID', [story_id])

        story = None
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                story = {
                    'id': row[0],
                    'user_id': row[1],
                    'username': row[2],
                    'profile_pic': row[3],
                    'media_url': row[4],
                    'media_type': row[5],
                    'duration': row[6],
                    'created_at': row[7],
                }
        con.close()

        if not story:
            return HttpResponse("Story not found.", status=404)

        return render(request, 'stories/story_detail.html', {
            'story': story,
            'current_time': timezone.now()
        })


class UploadStoryView(View):
    @login_required_session
    def get(self, request):
        return render(request, 'stories/upload_story.html')

    @login_required_session
    def post(self, request):
        media_type = request.POST['media_type']
        duration = int(request.POST.get('duration', 30))

        uploaded_file = request.FILES['media']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        user_id = request.session.get('user_id')
        story_ops.create_story(user_id, file_url, media_type, duration)

        return redirect('story_list')


class LikeStoryView(View):
    @login_required_session
    def get(self, request, story_id):
        user_id = request.session.get('user_id')
        story_ops.add_story_like(user_id, story_id)
        return redirect('story_detail', story_id=story_id)


class ReplyStoryView(View):
    @login_required_session
    def post(self, request, story_id):
        message = request.POST['message']
        user_id = request.session.get('user_id')
        story_ops.add_story_reply(user_id, story_id, message)
        return redirect('story_detail', story_id=story_id)


# -------------------- Profile Views --------------------

class ProfileView(View):
    @login_required_session
    def get(self, request):
        user_id = request.session.get('user_id')
        user = user_ops.get_user_by_id(user_id)
        stories = story_ops.get_user_stories(user_id)
        return render(request, 'stories/profile.html', {'user': user, 'stories': stories})


class EditProfileView(View):
    @login_required_session
    def get(self, request):
        user_id = request.session.get('user_id')
        user = user_ops.get_user_by_id(user_id)
        return render(request, 'stories/edit_profile.html', {'user': user})

    @login_required_session
    def post(self, request):
        user_id = request.session.get('user_id')
        full_name = request.POST['full_name']

        profile_pic = user_ops.get_user_by_id(user_id)['profile_pic']
        if 'profile_pic' in request.FILES:
            uploaded_file = request.FILES['profile_pic']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
            filename = fs.save(uploaded_file.name, uploaded_file)
            profile_pic = fs.url(filename)

        user_ops.update_user_profile(user_id, full_name, profile_pic)
        return redirect('profile')
