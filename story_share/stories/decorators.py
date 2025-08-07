# stories/decorators.py
from django.shortcuts import redirect

def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')  # change 'login' if your login URL name is different
        return view_func(request, *args, **kwargs)
    return wrapper
