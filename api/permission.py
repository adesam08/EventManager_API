from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, 'organizer'):
            organizer = obj.organizer
        elif hasattr(obj, 'event'):
            organizer = obj.event.organizer
        else:
            return False

        return organizer.user == request.user
