from rest_framework.permissions import BasePermission

from app.utils import identity_user
from django.contrib.auth.models import User

from rest_framework import exceptions
from rest_framework import authentication

from .redis import session_storage


# class AuthBySessionID(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         session_id = request.COOKIES.get("session_id")
#         if session_id is None:
#             raise exceptions.AuthenticationFailed('No session_id')

#         try:
#             username = session_storage.get(session_id).decode('utf-8')
#         except Exception as e:
#             raise exceptions.AuthenticationFailed('session_id not found')

#         user = User.objects.get(username=username)
#         if user is None:
#             raise exceptions.AuthenticationFailed('No such user')

#         return user, None


class AuthBySessionIDIfExists(authentication.BaseAuthentication):
    def authenticate(self, request):
        session_id = request.COOKIES.get("session_id")
        if session_id is None:
            return None, None
        try:
            username = session_storage.get(session_id).decode('utf-8')
        except Exception as e:
            return None, None
        #print(username)
        user = User.objects.get(pk=username)
        return user, None


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get("session_id")
        if session_id is None:
            return False
        try:
            session_storage.get(session_id).decode('utf-8')
        except Exception as e:
            return False
        return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get("session_id")
        if session_id is None:
            return False
        try:
            username = session_storage.get(session_id).decode('utf-8')
        except Exception as e:
            return False

        #print(username)
        user = User.objects.filter(pk=username).first()
        if user is None:
            return False

        return user.is_staff
