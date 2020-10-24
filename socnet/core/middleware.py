from django.urls import reverse
from django.utils.timezone import now
from django.contrib import auth
from rest_framework import status
from core.models import Member


def user_last_activity_mw(get_response):
    
    def f(request):
        if request.user.is_authenticated:
            user = Member.objects.select_for_update().filter(user=request.user)[0]
            user.last_request = now()
            user.save()

        response = get_response(request)
        return response
    
    return f
