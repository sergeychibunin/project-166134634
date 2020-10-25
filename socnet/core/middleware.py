from django.urls import reverse
from django.utils.timezone import now
from django.contrib import auth
from rest_framework import status
from core.models import Member


def user_last_activity_mw(get_response):
    
    def f(request):
        response = get_response(request)
        
        if request.user.is_authenticated:
            user_qs = Member.objects.select_for_update().filter(user=request.user)
            if len(user_qs):
                user = user_qs[0]
                user.last_request = now()
                user.save()
            else:
                user = Member(last_request=now(), user=request.user)
                user.save()

        return response
    
    return f
