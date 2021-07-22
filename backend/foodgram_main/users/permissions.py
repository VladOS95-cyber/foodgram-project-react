from rest_framework import permissions


class UserDetailedAuthOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return view.action != 'retrieve' or request.user and request.user.is_authenticated
