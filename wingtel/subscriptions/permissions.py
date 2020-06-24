from rest_framework.permissions import BasePermission


class SubscriptionBelongsToUser(BasePermission):
    """
    Check if subscription to activate
    """
    message = 'You don\'t have access to this subscription.'

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
