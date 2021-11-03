from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class CustomUserPermission(BasePermission):

    def has_permission(self, request, view):


        print(view.__dict__)
        
        if request.method == 'POST' and request.user.is_anonymous:
            return True
        elif request.method == 'GET':
            if request.user.is_authenticated:
                return True
            else:
                if view.action == 'retrieve':
                    return False
                else:
                    return True
        return False

    
