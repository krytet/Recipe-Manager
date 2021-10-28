from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class CustomUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_anonymous:
            return True
        elif request.method == 'GET' and request.user.is_authenticated:
            return True

        return False
    
