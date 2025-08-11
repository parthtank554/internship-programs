# stories/decorators.py
from django.shortcuts import redirect
from functools import wraps

def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        # If class-based view, first arg is 'self', request is self.request
        if hasattr(args[0], 'request'):
            request = args[0].request
        else:  # function-based view
            request = args[0]

        if 'user_id' not in request.session:
            return redirect('login')  # change 'login' if your login URL name is different
        return view_func(request, *args, **kwargs)
    return wrapper
