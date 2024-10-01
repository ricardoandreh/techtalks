from rest_framework.permissions import BasePermission


class IsOrganizerOfEvent(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.event.organizer == request.user
