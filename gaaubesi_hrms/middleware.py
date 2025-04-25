from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.contrib.auth import logout

class RestrictUserMiddleware(object):
    login_url = 'login'
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # restricted url not request.path.find("/login") > -1 and not request.path.find("/change-password") > -1 and not request.path.find("/track-order") and not request.path.find("/api")
        if request.path.find("/login") > -1 or request.path.find("/admin") > -1 or request.path.find("/logout") > -1:
            response = self.get_response(request)
            return response

        if not request.user.is_authenticated:
            # check for role admin or role
            return redirect_to_login(request.get_full_path(), reverse('login'), REDIRECT_FIELD_NAME)
            # return redirect_to_login(request.get_full_path(), resolve_url(self.login_url), REDIRECT_FIELD_NAME)

        # if request.user.profile.role != 'Super-Admin':
        #     messages.error(request, 'You do not have permission to view this page')
        #     logout(request)
        #     return redirect(reverse('login'))
        
        response = self.get_response(request)

        return response