from django.urls import reverse
from django.utils.timezone import now
from django.contrib import auth
from rest_framework import status
from core.models import Member


def user_auth_mw(get_response):
    
    def f(request):
        if not request.user.is_authenticated:
            is_anonymous = True
        else:
            is_anonymous = False

        response = get_response(request)
        if request.path == reverse('token_obtain_pair'):
            if is_anonymous and response.status_code == status.HTTP_200_OK:
                user = auth.get_user(response)
        return response
    
    return f
