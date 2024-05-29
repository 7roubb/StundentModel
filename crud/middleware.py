import time
from django.conf import settings
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = time.time()
            last_activity = request.session.get('last_activity', current_time)
            session_expiry = settings.SESSION_COOKIE_AGE

            if current_time - last_activity > session_expiry:
                request.session.flush()  
                return redirect('login')  

            request.session['last_activity'] = current_time  

        response = self.get_response(request)
        return response