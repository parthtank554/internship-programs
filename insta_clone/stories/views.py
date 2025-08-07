from django.shortcuts import render, redirect
from .operations import operations
from django.core.files.storage import FileSystemStorage


def story_list(request):
    stories = operations.get_active_stories()
    return render(request, 'storyapp/story_list.html', {'stories': stories})

def story_detail(request, story_id):
    user_id = request.user.id
    operations.add_story_view(user_id, story_id)
    data = operations.get_story_details(story_id)
    return render(request, 'storyapp/story_detail.html', data)

def upload_story(request):
    if request.method == 'POST':
        media_type = request.POST['media_type']
        duration = int(request.POST.get('duration', 0)) if media_type == 'video' else 0

        # Save uploaded file to static/media (you can configure MEDIA_ROOT)
        uploaded_file = request.FILES['media_url']
        fs = FileSystemStorage(location='media/')  # or settings.MEDIA_ROOT
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        operations.create_story(request.user.id, file_url, media_type, duration)
        return redirect('story_list')
    return render(request, 'storyapp/upload_story.html')


def like_story(request, story_id):
    operations.add_story_like(request.user.id, story_id)
    return redirect('story_detail', story_id=story_id)

def reply_story(request, story_id):
    if request.method == 'POST':
        message = request.POST['message']
        operations.add_story_reply(request.user.id, story_id, message)
    return redirect('story_detail', story_id=story_id)
